"""Validate graph structure and audit records, not the truth of a hypothesis."""

from __future__ import annotations

import argparse
import html
import json
import sys
import textwrap
from functools import lru_cache
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

NON_EVIDENCE_TYPES = {"MethodNode", "NarrativeNode", "NarrativeTraceNode"}
SUPPORT_RELATIONS = {"supports", "supports_weakly"}
CHECKED_STATUSES = {"pass", "warn", "fail"}
REFERENCE_TYPES = {
    "source": None,
    "source_paper": {"PaperNode"},
    "supporting_sources": None,
    "related_target_papers": {"PaperNode"},
    "related_target_narratives": {"NarrativeNode"},
    "target_narrative": {"NarrativeNode"},
    "risks": {"RiskNode"},
    "falsifiers": {"FalsifierNode"},
    "depends_on": None,
    "located_in": None,
    "would_weaken": None,
}
EVIDENCE_FIELDS = {"source", "source_paper", "supporting_sources", "related_target_papers"}


@lru_cache(maxsize=1)
def graph_validator() -> Draft202012Validator:
    schema_dir = Path(__file__).resolve().parent.parent / "schemas"
    resources = []
    graph_schema = None
    for name in ("node_schema.json", "edge_schema.json", "graph_schema.json"):
        path = schema_dir / name
        schema = json.loads(path.read_text(encoding="utf-8-sig"))
        schema["$id"] = path.as_uri()
        Draft202012Validator.check_schema(schema)
        resources.append((path.as_uri(), Resource.from_contents(schema)))
        if name == "graph_schema.json":
            graph_schema = schema
    # Resolve only bundled schemas. Validation never fetches remote resources.
    return Draft202012Validator(graph_schema, registry=Registry().with_resources(resources))


def schema_errors(data: object) -> list[str]:
    return sorted(
        f"Schema {'.'.join(map(str, error.absolute_path)) or '$'}: {error.message}"
        for error in graph_validator().iter_errors(data)
    )


def load_graph(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("Graph file must contain a JSON object.")
    return data


def field_refs(value: object) -> list[str]:
    return [value] if isinstance(value, str) else value or []


def is_recorded(value: object) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    value = value.strip().lower()
    return value not in {"unknown", "todo", "tbd", "...", "n/a"} and not value.startswith(
        ("replace", "not specified", "verification needed")
    )


def has_tier(node: dict, tier: str) -> bool:
    return tier in {node.get("tier"), node.get("proposed_tier"), node.get("declared_tier")}


def linked_falsifiers(node: dict, nodes: dict[str, dict], edges: list[dict]) -> set[str]:
    refs = set(node.get("falsifiers", []))
    refs.update(e["to"] for e in edges if e["from"] == node["node_id"] and e["relation"] == "falsified_by")
    return {ref for ref in refs if nodes.get(ref, {}).get("node_type") == "FalsifierNode"}


def validate_graph(data: object) -> list[str]:
    errors = schema_errors(data)
    if errors:
        return errors

    nodes: dict[str, dict] = {}
    for node in data["nodes"]:
        node_id = node["node_id"]
        if node_id in nodes:
            errors.append(f"Duplicate node_id: {node_id}")
        nodes[node_id] = node

    for node_id, node in nodes.items():
        for field, expected_types in REFERENCE_TYPES.items():
            for ref in field_refs(node.get(field)):
                target = nodes.get(ref)
                if target is None:
                    errors.append(f"Node {node_id}: {field} has unknown reference {ref}.")
                    continue
                target_type = target["node_type"]
                if expected_types and target_type not in expected_types:
                    errors.append(f"Node {node_id}: {field} must reference {'/'.join(sorted(expected_types))}, not {target_type} {ref}.")
                if field in EVIDENCE_FIELDS and target_type in NON_EVIDENCE_TYPES:
                    errors.append(f"Node {node_id}: {field} must not treat {target_type} {ref} as evidence.")

        if "declared_tier" in node:
            for field in ("tier_declared_by", "tier_declaration_ref", "tier_rationale"):
                if not is_recorded(node.get(field)):
                    errors.append(f"Node {node_id}: declared_tier requires a recorded {field}, not a placeholder.")
            if node["tier_declared_by"].strip().lower() in {"author", "expert", "reviewer", "operator", "ai", "llm", "assistant", "codex"}:
                errors.append(f"Node {node_id}: tier_declared_by must identify the human, not just a role or LLM.")
            if node.get("tier", "unknown") not in {"unknown", node["declared_tier"]}:
                errors.append(f"Node {node_id}: tier must match declared_tier; keep alternative candidates in proposed_tier.")
        elif "proposed_tier" in node and node.get("tier", "unknown") not in {"unknown", node["proposed_tier"]}:
            errors.append(f"Node {node_id}: tier and proposed_tier disagree without a human declaration.")

        if node["node_type"] == "UserClaimNode" and has_tier(node, "C"):
            if not linked_falsifiers(node, nodes, data["edges"]):
                errors.append(f"Node {node_id}: C-tier UserClaimNode must link to at least one FalsifierNode.")

    for idx, edge in enumerate(data["edges"]):
        src, dst, rel = edge["from"], edge["to"], edge["relation"]
        for role, ref in (("source", src), ("target", dst)):
            if ref not in nodes:
                errors.append(f"Edge {idx} has unknown {role} node: {ref}")
        source_type = nodes.get(src, {}).get("node_type")
        target_type = nodes.get(dst, {}).get("node_type")
        if rel in SUPPORT_RELATIONS and source_type in NON_EVIDENCE_TYPES:
            errors.append(f"Edge {idx}: {source_type} must not use {rel}; comparisons use heuristic_analogy_for.")
        if rel == "challenges_narrative" and target_type != "NarrativeNode":
            errors.append(f"Edge {idx}: challenges_narrative must target a NarrativeNode.")
        if rel == "heuristic_analogy_for" and source_type != "MethodNode":
            errors.append(f"Edge {idx}: heuristic_analogy_for must originate from a MethodNode.")
        if rel == "heuristic_analogy_for" and edge.get("support_strength", "analogy_only") not in {"analogy_only", "unknown"}:
            errors.append(f"Edge {idx}: an analogy must not claim evidentiary support_strength.")
        if rel == "falsified_by" and target_type != "FalsifierNode":
            errors.append(f"Edge {idx}: falsified_by points from the claim to a FalsifierNode.")

        source_ref = edge.get("source_ref")
        if source_ref is not None and nodes.get(source_ref, {}).get("node_type") != "PaperNode":
            errors.append(f"Edge {idx}: source_ref must reference a PaperNode.")
        if edge.get("local_check_status") in CHECKED_STATUSES:
            for field in ("source_span", "source_excerpt", "checked_by", "local_check_notes"):
                if not is_recorded(edge.get(field)):
                    errors.append(f"Edge {idx}: completed local check requires a recorded {field}; use needs_source until inspected.")
            if nodes.get(source_ref, {}).get("verification_status") != "verified":
                errors.append(f"Edge {idx}: completed local check requires a verified source_ref; use needs_source.")
            if edge["support_strength"] == "unknown":
                errors.append(f"Edge {idx}: completed local check needs a support finding, not unknown.")
        if edge.get("local_check_status") == "pass" and rel in SUPPORT_RELATIONS:
            if edge["support_strength"] in {"counter_example", "analogy_only", "no_direct_support"} or edge.get("claim_scope_match") == "mismatch":
                errors.append(f"Edge {idx}: pass conflicts with the local support finding; retain it as warn/fail.")
        if edge.get("local_check_status") == "needs_source" and edge.get("support_strength", "unknown") not in {"unknown", "analogy_only", "no_direct_support"}:
            errors.append(f"Edge {idx}: needs_source must not assert checked support_strength.")
    return errors


def audit_warnings(data: dict) -> list[str]:
    if schema_errors(data):
        return []
    warnings = []
    nodes = {node["node_id"]: node for node in data["nodes"]}
    for node_id, node in nodes.items():
        if node["node_type"] != "UserClaimNode":
            continue
        if "declared_tier" not in node:
            warnings.append(f"Node {node_id}: tier is provisional; human declaration is pending.")
        if not node["supporting_sources"]:
            warnings.append(f"Node {node_id}: no supporting sources recorded; this is citation debt, not proof of falsehood.")
        if has_tier(node, "C"):
            for ref in sorted(linked_falsifiers(node, nodes, data["edges"])):
                if "test_plan" not in nodes[ref]:
                    warnings.append(f"Node {node_id}: falsifier {ref} needs a measurement, weakening result, and alternative explanation.")
    for idx, edge in enumerate(data["edges"]):
        if edge["relation"] in SUPPORT_RELATIONS | {"contradicts"} and edge.get("local_check_status") not in CHECKED_STATUSES:
            warnings.append(f"Edge {idx} ({edge['from']} -> {edge['to']}): local source check pending.")
    return warnings


def label_for(node: dict) -> str:
    text = node["text"].replace("\n", " ")
    if len(text) > 80:
        text = text[:77] + "..."
    tier = node.get("declared_tier") or node.get("proposed_tier") or node.get("tier")
    status = node.get("tier_review_status", "proposed") if "declared_tier" in node else "proposed"
    prefix = f"{node['node_id']} {tier} ({status}): " if tier and tier != "unknown" else f"{node['node_id']}: "
    rows = [prefix.rstrip()] + textwrap.wrap(text, width=36, break_long_words=False, break_on_hyphens=False)
    safe = "<br/>".join(html.escape(row, quote=True).replace("[", "(").replace("]", ")") for row in rows)
    return f'{node["node_id"]}["{safe}"]'


def relation_label(rel: str) -> str:
    return {"supports_weakly": "weakly supports", "heuristic_analogy_for": "heuristic analogy", "falsified_by": "would be weakened by"}.get(rel, rel.replace("_", " "))


def render_mermaid(data: dict, grouped: bool = False) -> str:
    lines = ["graph TD"]
    if grouped:
        lines.insert(0, '%%{init: {"flowchart": {"defaultRenderer": "elk"}}}%%')
        clusters: dict[str, list[dict]] = {}
        for node in data["nodes"]:
            cluster = node.get("metadata", {}).get("cluster", "Unassigned")
            clusters.setdefault(str(cluster), []).append(node)
        for idx, (cluster, nodes) in enumerate(clusters.items()):
            lines.append(f'  subgraph cluster_{idx}["{html.escape(cluster, quote=True)}"]')
            lines.extend(f"    {label_for(node)}" for node in nodes)
            lines.append("  end")
    else:
        lines.extend(f"  {label_for(node)}" for node in data["nodes"])
    for edge in data["edges"]:
        rel = relation_label(edge["relation"])
        status = edge.get("local_check_status")
        if edge["relation"] in SUPPORT_RELATIONS | {"contradicts"}:
            rel += f" ({status or 'needs_source'})"
        dotted = status != "pass" or edge["relation"] in {"heuristic_analogy_for", "not_direct_evidence", "falsified_by", "qualifies"}
        arrow = f'-. "{rel}" .->' if dotted else f'-- "{rel}" -->'
        lines.append(f"  {edge['from']} {arrow} {edge['to']}")
    return "\n".join(lines)


def print_warnings(data: dict) -> None:
    warnings = audit_warnings(data)
    for warning in warnings[:10]:
        print(f"WARN: {warning}", file=sys.stderr)
    if len(warnings) > 10:
        print(f"WARN: {len(warnings) - 10} more pending audit findings; run audit for the full list.", file=sys.stderr)


def cmd_validate(args: argparse.Namespace) -> int:
    data = load_graph(Path(args.file))
    errors = validate_graph(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print_warnings(data)
    print("Graph structure and audit records are valid. This is not source verification or a truth verdict.")
    return 0


def cmd_render(args: argparse.Namespace) -> int:
    data = load_graph(Path(args.file))
    errors = validate_graph(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print_warnings(data)
    print(render_mermaid(data, grouped=args.grouped))
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    data = load_graph(Path(args.file))
    errors = validate_graph(data)
    print(json.dumps({"errors": errors, "warnings": audit_warnings(data)}, indent=2))
    return int(bool(errors))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="egm", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name, function in (("validate", cmd_validate), ("render", cmd_render), ("audit", cmd_audit)):
        command = sub.add_parser(name)
        command.add_argument("file")
        command.set_defaults(func=function)
        if name == "render":
            command.add_argument("--mermaid", action="store_true", help="Render Mermaid (default)")
            command.add_argument("--grouped", action="store_true", help="Group nodes by metadata.cluster")
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

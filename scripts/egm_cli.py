"""Minimal CLI utilities for Epistemic Gap Mapper.

This is intentionally lightweight. It validates basic node/edge shape and
renders Mermaid graphs from a nodes JSON file.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ALLOWED_NODE_TYPES = {
    "PaperNode",
    "SourceClaimNode",
    "UserClaimNode",
    "EvidenceNode",
    "InferenceNode",
    "AssumptionNode",
    "NarrativeNode",
    "NarrativeTraceNode",
    "GapNode",
    "ExceptionNode",
    "RiskNode",
    "FalsifierNode",
    "MethodNode",
}

ALLOWED_RELATIONS = {
    "supports",
    "supports_weakly",
    "contradicts",
    "extends",
    "qualifies",
    "depends_on",
    "explains_gap",
    "challenges_narrative",
    "overclaims",
    "requires_test",
    "falsified_by",
    "heuristic_analogy_for",
    "not_direct_evidence",
}

ALLOWED_TIERS = {"A", "B", "C", "X", "M", "unknown"}
ALLOWED_TIER_REVIEW_STATUS = {
    "proposed",
    "declared",
    "reviewer_checked",
    "needs_review",
    "disputed",
    "unknown",
}
ALLOWED_FAILURE_MODES = {
    "evidence_laundering",
    "analogy_inflation",
    "narrative_capture",
    "falsifier_removal",
    "citation_debt",
    "scope_jump",
}

EDGE_ENUM_FIELDS = {
    "support_strength": {
        "direct",
        "hedged",
        "presupposed",
        "contextual",
        "counter_example",
        "analogy_only",
        "no_direct_support",
        "unknown",
    },
    "support_mode": {
        "empirical",
        "textual",
        "inferential",
        "methodological",
        "comparative",
        "narrative_trace",
    },
    "local_check_status": {"pass", "warn", "fail", "needs_source"},
    "claim_scope_match": {"full", "partial", "mismatch", "unknown"},
    "vocabulary_match": {"same_terms", "mapped_terms", "ambiguous", "mismatch"},
    "granularity_match": {"same_grain", "too_broad", "too_narrow", "atomized", "unknown"},
}

TYPE_REQUIRED_FIELDS = {
    "PaperNode": ["citation", "domain", "source_kind", "role", "verification_status"],
    "SourceClaimNode": ["source_paper", "domain", "confidence"],
    "UserClaimNode": [
        "tier",
        "domain",
        "supporting_sources",
        "related_target_papers",
        "related_target_narratives",
        "risks",
        "falsifiers",
    ],
    "EvidenceNode": ["source", "domain", "tier"],
    "InferenceNode": ["tier", "depends_on", "risks"],
    "AssumptionNode": ["tier", "risk_level"],
    "NarrativeNode": ["source_status", "citation_debt", "component_claims"],
    "NarrativeTraceNode": ["target_narrative", "source_paper", "trace_status", "citation_debt_effect"],
    "GapNode": ["located_in", "importance"],
    "ExceptionNode": ["target_narrative", "source"],
    "RiskNode": ["risky_phrase", "why_risky", "suggested_patch"],
    "FalsifierNode": ["would_weaken", "required_evidence"],
    "MethodNode": ["method_name", "not_evidence"],
}


def load_graph(path: Path) -> dict:
    with path.open("r", encoding="utf-8-sig") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("Graph file must contain a JSON object.")
    return data


def has_value(node: dict, field: str) -> bool:
    value = node.get(field)
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def field_refs(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []


def node_type_is(node_by_id: dict[str, dict], node_id: str, expected_type: str) -> bool:
    node = node_by_id.get(node_id)
    return bool(node and node.get("node_type") == expected_type)


def validate_graph(data: dict) -> list[str]:
    errors: list[str] = []
    nodes = data.get("nodes")
    edges = data.get("edges")

    if not isinstance(nodes, list):
        errors.append("Graph is missing nodes array.")
        nodes = []
    if not isinstance(edges, list):
        errors.append("Graph is missing edges array.")
        edges = []

    ids: set[str] = set()
    node_by_id: dict[str, dict] = {}
    for idx, node in enumerate(nodes):
        node_id = node.get("node_id")
        if not node_id:
            errors.append(f"Node at index {idx} is missing node_id.")
            continue
        if node_id in ids:
            errors.append(f"Duplicate node_id: {node_id}")
        ids.add(node_id)
        node_by_id[node_id] = node
        node_type = node.get("node_type")
        if node_type not in ALLOWED_NODE_TYPES:
            errors.append(f"Node {node_id} has invalid node_type: {node_type}")
        for tier_field in ("tier", "declared_tier"):
            if tier_field in node and node.get(tier_field) not in ALLOWED_TIERS:
                errors.append(f"Node {node_id} has invalid {tier_field}: {node.get(tier_field)}")
        if "tier_review_status" in node and node.get("tier_review_status") not in ALLOWED_TIER_REVIEW_STATUS:
            errors.append(f"Node {node_id} has invalid tier_review_status: {node.get('tier_review_status')}")
        if "failure_modes" in node:
            failure_modes = node.get("failure_modes")
            if not isinstance(failure_modes, list) or not failure_modes:
                errors.append(f"Node {node_id}: failure_modes must be a non-empty list.")
            else:
                for mode in failure_modes:
                    if mode not in ALLOWED_FAILURE_MODES:
                        errors.append(f"Node {node_id} has invalid failure_mode: {mode}")
        if not has_value(node, "text"):
            errors.append(f"Node {node_id} is missing text.")
        for field in TYPE_REQUIRED_FIELDS.get(node_type, []):
            if not has_value(node, field):
                errors.append(f"Node {node_id} ({node_type}) is missing {field}.")
        if node_type == "MethodNode" and node.get("not_evidence") is not True:
            errors.append(f"Node {node_id} (MethodNode) should set not_evidence to true.")
        if node_type == "UserClaimNode" and has_value(node, "declared_tier"):
            for field in ("tier_declared_by", "tier_rationale", "tier_review_status"):
                if not has_value(node, field):
                    errors.append(
                        f"Node {node_id}: declared_tier requires {field} so the human declaration remains visible."
                    )
        if "X" in {node.get("tier"), node.get("declared_tier")} and not has_value(node, "failure_modes"):
            errors.append(f"Node {node_id}: X-tier nodes must declare at least one failure_mode.")

    for node in nodes:
        node_id = node.get("node_id")
        node_type = node.get("node_type")
        for source_id in field_refs(node.get("supporting_sources")):
            source_node = node_by_id.get(source_id)
            if source_node and source_node.get("node_type") == "MethodNode":
                if node_type == "UserClaimNode":
                    errors.append(
                        f"Node {node_id}: UserClaimNode.supporting_sources must not reference MethodNode {source_id}; use heuristic_analogy_for edges instead."
                    )
                else:
                    errors.append(
                        f"Node {node_id}: supporting_sources must not treat MethodNode {source_id} as evidence."
                    )
        for field in ("source", "source_paper", "related_target_papers"):
            for source_id in field_refs(node.get(field)):
                source_node = node_by_id.get(source_id)
                if source_node and source_node.get("node_type") == "MethodNode":
                    errors.append(f"Node {node_id}: {field} must not reference MethodNode {source_id} as evidence.")

        if node_type == "UserClaimNode" and "C" in {node.get("tier"), node.get("declared_tier")}:
            falsifier_refs = [
                ref
                for ref in field_refs(node.get("falsifiers"))
                if node_type_is(node_by_id, ref, "FalsifierNode")
            ]
            falsifier_edges = [
                edge
                for edge in edges
                if edge.get("relation") == "falsified_by"
                and edge.get("to") == node_id
                and node_type_is(node_by_id, edge.get("from"), "FalsifierNode")
            ]
            if not falsifier_refs and not falsifier_edges:
                errors.append(
                    f"Node {node_id}: C-tier UserClaimNode must link to at least one FalsifierNode."
                )

    for idx, edge in enumerate(edges):
        src = edge.get("from")
        dst = edge.get("to")
        rel = edge.get("relation")
        if src not in ids:
            errors.append(f"Edge {idx} has unknown source node: {src}")
        if dst not in ids:
            errors.append(f"Edge {idx} has unknown target node: {dst}")
        if rel not in ALLOWED_RELATIONS:
            errors.append(f"Edge {idx} has invalid relation: {rel}")
        for field, allowed_values in EDGE_ENUM_FIELDS.items():
            if field in edge and edge.get(field) not in allowed_values:
                errors.append(f"Edge {idx} has invalid {field}: {edge.get(field)}")
        source_node = node_by_id.get(src)
        target_node = node_by_id.get(dst)
        if rel == "supports" and source_node and source_node.get("node_type") == "MethodNode":
            errors.append(
                f"Edge {idx}: Method/comparison nodes should not use supports; use heuristic_analogy_for."
            )
        if rel == "challenges_narrative" and target_node and target_node.get("node_type") != "NarrativeNode":
            errors.append(f"Edge {idx}: challenges_narrative must target a NarrativeNode.")
        if rel == "heuristic_analogy_for" and source_node and source_node.get("node_type") != "MethodNode":
            errors.append(f"Edge {idx}: heuristic_analogy_for should originate from a MethodNode.")
        if rel == "supports" and source_node and source_node.get("node_type") == "NarrativeNode":
            errors.append(f"Edge {idx}: NarrativeNode should not directly support claims; use SourceClaimNode or EvidenceNode.")
    return errors


def label_for(node: dict) -> str:
    text = node.get("text") or node.get("method_name") or node.get("node_id")
    text = text.replace("\n", " ")
    if len(text) > 80:
        text = text[:77] + "..."
    safe = text.replace('"', "'").replace("[", "(").replace("]", ")")
    return f'{node["node_id"]}["{safe}"]'


def relation_label(rel: str) -> str:
    labels = {
        "supports": "supports",
        "supports_weakly": "weakly supports",
        "contradicts": "contradicts",
        "extends": "extends",
        "qualifies": "qualifies",
        "depends_on": "depends on",
        "explains_gap": "explains gap",
        "challenges_narrative": "challenges narrative",
        "overclaims": "overclaims",
        "requires_test": "requires test",
        "falsified_by": "falsified by",
        "heuristic_analogy_for": "heuristic analogy",
        "not_direct_evidence": "not evidence",
    }
    return labels.get(rel, rel)


def render_mermaid(data: dict) -> str:
    node_map = {node["node_id"]: node for node in data.get("nodes", [])}
    lines = ["graph TD"]
    for node in data.get("nodes", []):
        lines.append(f"  {label_for(node)}")
    for edge in data.get("edges", []):
        src = edge["from"]
        dst = edge["to"]
        rel = relation_label(edge["relation"])
        if src in node_map and dst in node_map:
            lines.append(f"  {src} -- {rel} --> {dst}")
    return "\n".join(lines)


def cmd_validate(args: argparse.Namespace) -> int:
    data = load_graph(Path(args.file))
    errors = validate_graph(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Graph is valid.")
    return 0


def cmd_render(args: argparse.Namespace) -> int:
    data = load_graph(Path(args.file))
    errors = validate_graph(data)
    if errors and not args.force:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(render_mermaid(data))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="egm", description="Epistemic Gap Mapper helper CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="Validate a nodes JSON file")
    validate.add_argument("file")
    validate.set_defaults(func=cmd_validate)

    render = sub.add_parser("render", help="Render Mermaid graph from a nodes JSON file")
    render.add_argument("file")
    render.add_argument("--mermaid", action="store_true", help="Render as Mermaid graph output")
    render.add_argument("--force", action="store_true", help="Render even if validation errors exist")
    render.set_defaults(func=cmd_render)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

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


def load_graph(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("Graph file must contain a JSON object.")
    data.setdefault("nodes", [])
    data.setdefault("edges", [])
    return data


def validate_graph(data: dict) -> list[str]:
    errors: list[str] = []
    nodes = data.get("nodes", [])
    edges = data.get("edges", [])

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
        if not node.get("text") and node_type != "MethodNode":
            errors.append(f"Node {node_id} is missing text.")

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
        source_node = node_by_id.get(src)
        if rel == "supports" and source_node and source_node.get("node_type") == "MethodNode":
            errors.append(
                f"Edge {idx}: Method/comparison nodes should not use supports; use heuristic_analogy_for."
            )
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

"""Compatibility entry point; the skill's script is the single implementation."""

from scripts.egm_cli import (
    audit_warnings,
    label_for,
    load_graph,
    main,
    relation_label,
    render_mermaid,
    validate_graph,
)

__all__ = [
    "audit_warnings", "label_for", "load_graph", "main", "relation_label",
    "render_mermaid", "validate_graph",
]

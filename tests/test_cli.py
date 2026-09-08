import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.egm_cli import (
    audit_warnings, graph_validator, load_graph, render_mermaid, validate_graph,
)

ROOT = Path(__file__).resolve().parents[1]
CALIBRATION = ROOT / "examples/calibration_local_support/nodes_calibration.json"
SAMPLES = sorted((ROOT / "examples").rglob("nodes*.json")) + [ROOT / "templates/nodes_template.json"]


@pytest.fixture
def graph():
    return load_graph(CALIBRATION)


def node(graph, node_id):
    return next(n for n in graph["nodes"] if n["node_id"] == node_id)


def add_method(graph):
    graph["nodes"].append({
        "node_id": "M1", "node_type": "MethodNode", "text": "Analogy only.",
        "method_name": "Historical analogy", "not_evidence": True,
    })


@pytest.mark.parametrize("path", SAMPLES, ids=lambda p: p.relative_to(ROOT).as_posix())
def test_samples_use_schema_and_semantics(path):
    data = load_graph(path)
    assert list(graph_validator().iter_errors(data)) == []
    assert validate_graph(data) == []


def test_compatibility_entry_point_is_same_implementation():
    from egm import cli
    assert cli.validate_graph is validate_graph
    assert cli.render_mermaid is render_mermaid


@pytest.mark.parametrize("relation", ["supports", "supports_weakly"])
@pytest.mark.parametrize("source_id", ["M1", "N1", "NT1"])
def test_non_evidence_nodes_cannot_support(graph, source_id, relation):
    add_method(graph)
    graph["edges"].append({"from": source_id, "to": "UC1", "relation": relation})
    assert any("must not use" in error for error in validate_graph(graph))


@pytest.mark.parametrize("field,value", [
    ("supporting_sources", ["M1"]), ("source", "M1"),
    ("source_paper", "M1"), ("related_target_papers", ["M1"]),
])
def test_method_cannot_enter_evidence_fields(graph, field, value):
    add_method(graph)
    node(graph, "UC1")[field] = value
    assert any("as evidence" in error for error in validate_graph(graph))


@pytest.mark.parametrize("field,value", [
    ("supporting_sources", ["MISSING"]), ("source", ["P1", "MISSING"]),
    ("source_paper", "MISSING"), ("related_target_papers", ["MISSING"]),
    ("related_target_narratives", ["MISSING"]), ("falsifiers", ["MISSING"]),
    ("risks", ["MISSING"]), ("depends_on", ["MISSING"]),
])
def test_all_supplied_references_must_resolve(graph, field, value):
    node(graph, "UC1")[field] = value
    assert any("unknown reference MISSING" in error for error in validate_graph(graph))


@pytest.mark.parametrize("field,value", [
    ("related_target_papers", ["N1"]), ("related_target_narratives", ["P1"]),
    ("falsifiers", ["R1"]), ("risks", ["F1"]),
])
def test_reference_types_are_checked(graph, field, value):
    node(graph, "UC1")[field] = value
    assert any("must reference" in error for error in validate_graph(graph))


def test_empty_source_and_risk_lists_are_honest_valid_data(graph):
    node(graph, "UC1").update(supporting_sources=[], risks=[], falsifiers=[], related_target_narratives=[])
    assert validate_graph(graph) == []
    assert any("citation debt, not proof of falsehood" in w for w in audit_warnings(graph))


@pytest.mark.parametrize("tier_field", ["tier", "proposed_tier", "declared_tier"])
def test_c_requires_an_actual_falsifier(graph, tier_field):
    claim = node(graph, "UC3")
    claim["falsifiers"] = []
    graph["edges"] = [e for e in graph["edges"] if e["relation"] != "falsified_by"]
    claim["tier"] = "unknown"
    claim.pop("proposed_tier")
    claim[tier_field] = "C"
    if tier_field == "declared_tier":
        declare(claim, "C")
    assert any("C-tier" in error for error in validate_graph(graph))


def test_c_accepts_edge_only_or_reference_only_link(graph):
    node(graph, "UC3")["falsifiers"] = []
    assert validate_graph(graph) == []
    node(graph, "UC3")["falsifiers"] = ["F1"]
    graph["edges"] = [e for e in graph["edges"] if e["relation"] != "falsified_by"]
    assert validate_graph(graph) == []


def test_falsifier_direction_and_plan_warning(graph):
    edge = next(e for e in graph["edges"] if e["relation"] == "falsified_by")
    edge["from"], edge["to"] = edge["to"], edge["from"]
    assert any("points from the claim" in error for error in validate_graph(graph))
    edge["from"], edge["to"] = edge["to"], edge["from"]
    del node(graph, "F1")["test_plan"]
    assert validate_graph(graph) == []
    assert any("measurement" in w for w in audit_warnings(graph))


def declare(claim, tier="A"):
    claim.update(
        declared_tier=tier, tier=tier, tier_declared_by="fixture-reviewer-17",
        tier_declaration_ref="synthetic-review-log#decision-1",
        tier_rationale="Synthetic record used only to test the declaration contract.",
        tier_review_status="declared",
    )


def test_declaration_requires_bundle_and_actual_status(graph):
    claim = node(graph, "UC1")
    claim["declared_tier"] = "A"
    assert validate_graph(graph)
    declare(claim)
    assert validate_graph(graph) == []
    claim["tier_review_status"] = "proposed"
    assert validate_graph(graph)


@pytest.mark.parametrize("field", ["tier_declared_by", "tier_declaration_ref", "tier_rationale"])
def test_declaration_rejects_placeholder_records(graph, field):
    claim = node(graph, "UC1")
    declare(claim)
    claim[field] = "replace with actual record"
    assert any("placeholder" in error for error in validate_graph(graph))


def test_human_role_alone_is_not_identity(graph):
    claim = node(graph, "UC1")
    declare(claim)
    claim["tier_declared_by"] = "author"
    assert any("identify the human" in error for error in validate_graph(graph))


def test_declared_status_without_declaration_is_invalid(graph):
    node(graph, "UC1")["tier_review_status"] = "declared"
    assert validate_graph(graph)


def test_candidate_can_disagree_without_overwriting_human(graph):
    claim = node(graph, "UC1")
    declare(claim)
    claim["proposed_tier"] = "B"
    assert validate_graph(graph) == []
    assert "A (declared)" in render_mermaid(graph)


@pytest.mark.parametrize("field", ["source_ref", "source_span", "source_excerpt", "checked_by", "local_check_notes"])
def test_completed_check_requires_provenance(graph, field):
    del graph["edges"][0][field]
    assert validate_graph(graph)


@pytest.mark.parametrize("status", ["pass", "warn", "fail"])
def test_completed_check_requires_inspected_source(graph, status):
    node(graph, "P1")["verification_status"] = "verification needed"
    graph["edges"][0]["local_check_status"] = status
    assert any("verified source_ref" in error for error in validate_graph(graph))


@pytest.mark.parametrize("value", ["", "not specified in sample", "TODO"])
def test_placeholder_source_span_cannot_pass(graph, value):
    graph["edges"][0]["source_span"] = value
    assert any("recorded source_span" in error for error in validate_graph(graph))


def test_pending_source_cannot_claim_direct_support(graph):
    graph["edges"][0]["local_check_status"] = "needs_source"
    assert any("must not assert checked support_strength" in e for e in validate_graph(graph))
    graph["edges"][0]["support_strength"] = "unknown"
    assert validate_graph(graph) == []


def test_pass_cannot_hide_a_scope_mismatch(graph):
    graph["edges"][0]["claim_scope_match"] = "mismatch"
    assert any("pass conflicts" in error for error in validate_graph(graph))


def test_failing_local_check_does_not_change_tiers(graph):
    before = copy.deepcopy(graph)
    assert graph["edges"][1]["local_check_status"] == "fail"
    assert validate_graph(graph) == []
    assert graph == before


def test_calibration_excerpts_are_in_the_supplied_source(graph):
    source = (CALIBRATION.parent / "source.md").read_text(encoding="utf-8")
    for edge in graph["edges"]:
        if edge.get("local_check_status") in {"pass", "warn", "fail"}:
            assert edge["source_excerpt"] in source
            assert edge["source_ref"] == "P1"
    assert "fictional fixture" in source


@pytest.mark.parametrize("data", [
    None, [], {}, {"nodes": [None], "edges": []},
    {"nodes": [], "edges": [None]},
    {"nodes": [{"node_id": [], "node_type": {}, "text": "x"}], "edges": []},
])
def test_malformed_shapes_return_diagnostics_not_exceptions(data):
    assert validate_graph(data)


@pytest.mark.parametrize("field,value", [
    ("tier", {}), ("failure_modes", [{}]), ("supporting_sources", [None]),
    ("metadata", "wrong"), ("text", "   "), ("node_id", "bad-->id"),
])
def test_malformed_node_fields_are_schema_errors(graph, field, value):
    node(graph, "UC2")[field] = value
    assert any(e.startswith("Schema") for e in validate_graph(graph))


def test_duplicate_modes_and_ids_are_rejected(graph):
    node(graph, "UC2")["failure_modes"] = ["scope_jump", "scope_jump"]
    assert validate_graph(graph)
    node(graph, "UC2")["failure_modes"] = ["scope_jump"]
    graph["nodes"].append(copy.deepcopy(node(graph, "P1")))
    assert any("Duplicate node_id" in e for e in validate_graph(graph))


def test_method_not_evidence_is_schema_constraint(graph):
    add_method(graph)
    node(graph, "M1")["not_evidence"] = False
    assert any(e.startswith("Schema") for e in validate_graph(graph))


def test_relation_targets_and_analogy_metadata(graph):
    graph["edges"].append({"from": "UC1", "to": "P1", "relation": "challenges_narrative"})
    assert any("must target a NarrativeNode" in e for e in validate_graph(graph))
    graph["edges"].pop()
    add_method(graph)
    graph["edges"].append({"from": "M1", "to": "UC1", "relation": "heuristic_analogy_for", "support_strength": "direct"})
    assert any("analogy must not claim" in e for e in validate_graph(graph))


def test_render_exposes_candidates_and_pending_checks(graph):
    graph["edges"][0]["local_check_status"] = "needs_source"
    graph["edges"][0]["support_strength"] = "unknown"
    rendered = render_mermaid(graph, grouped=True)
    assert "A (proposed)" in rendered
    assert "supports (needs_source)" in rendered
    assert 'UC3 -. "would be weakened by" .-> F1' in rendered
    assert "subgraph cluster_" in rendered


@pytest.mark.parametrize("entry", [["scripts/egm_cli.py"], ["-m", "egm"]])
def test_cli_entry_points_and_audit_json(entry):
    result = subprocess.run([sys.executable, "-B", *entry, "audit", str(CALIBRATION)], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    result = json.loads(result.stdout)
    assert result["errors"] == []
    assert result["warnings"]


def test_cli_invalid_json_is_concise(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("{broken", encoding="utf-8")
    result = subprocess.run([sys.executable, "-B", "scripts/egm_cli.py", "validate", str(path)], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 1
    assert "ERROR:" in result.stderr
    assert "Traceback" not in result.stderr


@pytest.mark.parametrize("json_path,diagram_path,grouped", [
    ("examples/jomon_dotaku_kiki/nodes_full.json", "examples/jomon_dotaku_kiki/graph_sample_grouped.md", True),
    ("examples/jomon_dotaku_kiki/nodes_sample.json", "examples/jomon_dotaku_kiki/graph_sample.md", False),
    ("examples/starter_cafe_rain/nodes_starter.json", "examples/starter_cafe_rain/graph_starter.md", False),
    ("examples/calibration_local_support/nodes_calibration.json", "examples/calibration_local_support/graph_calibration.md", False),
    ("templates/nodes_template.json", "templates/graph_template.md", False),
])
def test_generated_diagrams_match_graph_data(json_path, diagram_path, grouped):
    document = (ROOT / diagram_path).read_text(encoding="utf-8")
    diagram = document.split("```mermaid\n", 1)[1].split("\n```", 1)[0]
    assert diagram == render_mermaid(load_graph(ROOT / json_path), grouped=grouped)

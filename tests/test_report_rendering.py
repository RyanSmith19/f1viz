from f1viz.reports.renderers import render_markdown
from f1viz.services.demo_reports import build_demo_race_report


def test_demo_report_serializes_to_json() -> None:
    report = build_demo_race_report(year=2025, grand_prix="Monaco")

    payload = report.model_dump()

    assert payload["report_type"] == "race_analysis"
    assert payload["year"] == 2025
    assert payload["grand_prix"] == "Monaco"
    assert payload["sections"][0]["confidence"] == "high"
    assert payload["timeline"][0]["elapsed_seconds"] == 0


def test_markdown_renderer_includes_evidence_and_timeline() -> None:
    report = build_demo_race_report(year=2025, grand_prix="Monaco")

    markdown = render_markdown(report)

    assert "# 2025 Monaco Race Report" in markdown
    assert "## Replay Timeline" in markdown
    assert "00:00:00 - Race replay initialized" in markdown
    assert "Evidence:" in markdown
    assert "docs/product/assumptions.md" in markdown


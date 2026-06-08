from pathlib import Path
from typing import Annotated

import typer

from f1viz.reports.renderers import render_markdown
from f1viz.services.demo_reports import build_demo_race_report

app = typer.Typer(help="F1 race replay and storytelling analytics.")
race_app = typer.Typer(help="Race analysis commands.")
app.add_typer(race_app, name="race")


@app.callback()
def main() -> None:
    """F1Viz command-line interface."""


@race_app.command("analyze")
def analyze_race(
    year: Annotated[int, typer.Option(help="F1 season year.")],
    gp: Annotated[str, typer.Option(help="Grand Prix slug or name.")],
    output_dir: Annotated[
        Path,
        typer.Option(help="Directory for generated Markdown and JSON reports."),
    ] = Path("reports"),
) -> None:
    """Create a whole-race report.

    This command currently writes a scaffold report. OpenF1 loading and real analysis
    will replace the demo service while preserving the output contract.
    """
    report = build_demo_race_report(year=year, grand_prix=gp)
    output_dir.mkdir(parents=True, exist_ok=True)

    stem = f"{year}-{gp.lower().replace(' ', '-')}-race-analysis"
    json_path = output_dir / f"{stem}.json"
    markdown_path = output_dir / f"{stem}.md"

    json_path.write_text(report.model_dump_json(indent=2), encoding="utf-8")
    markdown_path.write_text(render_markdown(report), encoding="utf-8")

    typer.echo(f"Wrote {markdown_path}")
    typer.echo(f"Wrote {json_path}")


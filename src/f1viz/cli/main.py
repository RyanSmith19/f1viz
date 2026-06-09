from pathlib import Path
from typing import Annotated

import typer

from f1viz.openf1 import OpenF1Client, OpenF1Endpoint
from f1viz.reports.renderers import render_markdown
from f1viz.repositories.fixture_repository import FixtureRepository
from f1viz.services.demo_reports import build_demo_race_report
from f1viz.services.driver_comparison import DriverComparisonService
from f1viz.services.driver_comparison_report_builder import DriverComparisonReportBuilder
from f1viz.services.race_report_builder import RaceReportBuilder
from f1viz.services.race_session_builder import RaceSessionBuilder
from f1viz.services.session_data_loader import CORE_RACE_ENDPOINTS, SessionDataLoader
from f1viz.services.session_fixture_reader import SessionFixtureReader
from f1viz.services.session_fixture_writer import SessionFixtureWriter

app = typer.Typer(help="F1 race replay and storytelling analytics.")
race_app = typer.Typer(help="Race analysis commands.")
fixtures_app = typer.Typer(help="OpenF1 fixture commands.")
app.add_typer(race_app, name="race")
app.add_typer(fixtures_app, name="fixtures")


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
    fixture_name: Annotated[
        str | None,
        typer.Option(help="Optional fixture name to analyze without network."),
    ] = None,
    fixtures_dir: Annotated[
        Path,
        typer.Option(help="Directory containing endpoint fixtures."),
    ] = Path("tests/fixtures/openf1"),
) -> None:
    """Create a whole-race report.

    This command currently writes a scaffold report. OpenF1 loading and real analysis
    will replace the demo service while preserving the output contract.
    """
    if fixture_name:
        raw_data = SessionFixtureReader(FixtureRepository(fixtures_dir)).load(name=fixture_name)
        race_session = RaceSessionBuilder().build(raw_data)
        report = RaceReportBuilder().build(race_session)
    else:
        report = build_demo_race_report(year=year, grand_prix=gp)
    output_dir.mkdir(parents=True, exist_ok=True)

    stem = f"{year}-{gp.lower().replace(' ', '-')}-race-analysis"
    json_path = output_dir / f"{stem}.json"
    markdown_path = output_dir / f"{stem}.md"

    json_path.write_text(report.model_dump_json(indent=2), encoding="utf-8")
    markdown_path.write_text(render_markdown(report), encoding="utf-8")

    typer.echo(f"Wrote {markdown_path}")
    typer.echo(f"Wrote {json_path}")


@race_app.command("compare")
def compare_drivers(
    year: Annotated[int, typer.Option(help="F1 season year.")],
    gp: Annotated[str, typer.Option(help="Grand Prix slug or name.")],
    first_driver: Annotated[str, typer.Option(help="First driver acronym or number.")],
    second_driver: Annotated[str, typer.Option(help="Second driver acronym or number.")],
    fixture_name: Annotated[
        str,
        typer.Option(help="Fixture name to analyze without network."),
    ],
    output_dir: Annotated[
        Path,
        typer.Option(help="Directory for generated Markdown and JSON reports."),
    ] = Path("reports"),
    fixtures_dir: Annotated[
        Path,
        typer.Option(help="Directory containing endpoint fixtures."),
    ] = Path("tests/fixtures/openf1"),
) -> None:
    """Compare two drivers using fixture-backed race facts."""
    raw_data = SessionFixtureReader(FixtureRepository(fixtures_dir)).load(name=fixture_name)
    race_session = RaceSessionBuilder().build(raw_data)
    comparison = DriverComparisonService().compare(race_session, first_driver, second_driver)
    report = DriverComparisonReportBuilder().build(
        meeting=race_session.meeting,
        session=race_session.session,
        comparison=comparison,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    stem = (
        f"{year}-{gp.lower().replace(' ', '-')}-"
        f"{first_driver.lower()}-{second_driver.lower()}-comparison"
    )
    json_path = output_dir / f"{stem}.json"
    markdown_path = output_dir / f"{stem}.md"

    json_path.write_text(report.model_dump_json(indent=2), encoding="utf-8")
    markdown_path.write_text(render_markdown(report), encoding="utf-8")

    typer.echo(f"Wrote {markdown_path}")
    typer.echo(f"Wrote {json_path}")


@fixtures_app.command("record")
def record_fixtures(
    year: Annotated[int, typer.Option(help="F1 season year.")],
    gp: Annotated[str, typer.Option(help="Grand Prix slug or name.")],
    session_name: Annotated[str, typer.Option(help="OpenF1 session name.")] = "Race",
    fixtures_dir: Annotated[
        Path,
        typer.Option(help="Directory where endpoint fixtures are written."),
    ] = Path("tests/fixtures/openf1"),
) -> None:
    """Record raw OpenF1 fixtures for a race session.

    This command uses the network and is intentionally separate from default tests.
    """
    loader = SessionDataLoader(OpenF1Client())
    data = loader.load(
        year=year,
        grand_prix=gp,
        session_name=session_name,
        endpoints=CORE_RACE_ENDPOINTS,
    )
    fixture_name = f"{year}-{gp.lower().replace(' ', '-')}-{session_name.lower().replace(' ', '-')}"
    writer = SessionFixtureWriter(FixtureRepository(fixtures_dir))
    paths = writer.save(data, name=fixture_name)

    typer.echo(
        f"Recorded {sum(data.counts_by_endpoint().values())} rows across "
        f"{len(data.records)} endpoints."
    )
    for path in paths:
        typer.echo(f"Wrote {path}")


@fixtures_app.command("endpoints")
def list_fixture_endpoints() -> None:
    """List core endpoints recorded for race analysis fixtures."""
    for endpoint in [OpenF1Endpoint.MEETINGS, OpenF1Endpoint.SESSIONS, *CORE_RACE_ENDPOINTS]:
        typer.echo(endpoint.value)


@fixtures_app.command("summary")
def summarize_fixture(
    name: Annotated[str, typer.Option(help="Fixture name, such as 2025-monaco-race.")],
    fixtures_dir: Annotated[
        Path,
        typer.Option(help="Directory containing endpoint fixtures."),
    ] = Path("tests/fixtures/openf1"),
) -> None:
    """Summarize a saved fixture set without using the network."""
    reader = SessionFixtureReader(FixtureRepository(fixtures_dir))
    data = reader.load(name=name)

    typer.echo(f"Meeting: {data.meeting.year} {data.meeting.meeting_name}")
    typer.echo(f"Session: {data.session.session_name} ({data.session.session_key})")
    typer.echo("Records:")
    for endpoint, count in sorted(data.counts_by_endpoint().items()):
        typer.echo(f"- {endpoint}: {count}")

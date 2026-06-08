from f1viz.models.reports import Confidence, Evidence, RaceReport, ReplayEvent, ReportSection


def build_demo_race_report(year: int, grand_prix: str) -> RaceReport:
    """Build the initial report contract before OpenF1 analysis is implemented."""
    return RaceReport(
        year=year,
        grand_prix=grand_prix,
        executive_summary=(
            "This scaffold report preserves the Markdown and JSON contract for future "
            "OpenF1-backed race replay analysis."
        ),
        sections=[
            ReportSection(
                title="Analysis Contract",
                summary=(
                    "Future reports will explain race performance using conservative, "
                    "evidence-backed comparisons against teammate, field median, session "
                    "leader, and own-best baselines."
                ),
                evidence=[
                    Evidence(
                        label="Product assumption",
                        detail="Driver comparisons must include contextual baselines.",
                        source="docs/product/assumptions.md",
                    )
                ],
                confidence=Confidence.HIGH,
            )
        ],
        timeline=[
            ReplayEvent(
                elapsed_seconds=0,
                title="Race replay initialized",
                category="system",
                summary=(
                    "The time-based replay model is available. Real OpenF1 event detection "
                    "will populate this timeline in later phases."
                ),
                evidence=[
                    Evidence(
                        label="Roadmap phase",
                        detail="Time-based replay CLI is planned as a first-class feature.",
                        source="docs/roadmaps/roadmap-cli.md",
                    )
                ],
                confidence=Confidence.HIGH,
            )
        ],
    )


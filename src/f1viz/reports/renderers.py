from f1viz.models.reports import RaceReport


def _format_elapsed(seconds: float) -> str:
    total_seconds = int(seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def render_markdown(report: RaceReport) -> str:
    lines = [
        f"# {report.year} {report.grand_prix} {report.session_name} Report",
        "",
        "## Summary",
        "",
        report.executive_summary,
        "",
    ]

    if report.sections:
        lines.extend(["## Analysis", ""])
        for section in report.sections:
            lines.extend(
                [
                    f"### {section.title}",
                    "",
                    section.summary,
                    "",
                    f"Confidence: {section.confidence.value}",
                    "",
                ]
            )
            if section.evidence:
                lines.append("Evidence:")
                for evidence in section.evidence:
                    lines.append(f"- {evidence.label}: {evidence.detail} ({evidence.source})")
                lines.append("")

    if report.timeline:
        lines.extend(["## Replay Timeline", ""])
        for event in sorted(report.timeline, key=lambda item: item.elapsed_seconds):
            lines.extend(
                [
                    f"### {_format_elapsed(event.elapsed_seconds)} - {event.title}",
                    "",
                    event.summary,
                    "",
                    f"Category: {event.category}",
                    f"Confidence: {event.confidence.value}",
                    "",
                ]
            )
            if event.evidence:
                lines.append("Evidence:")
                for evidence in event.evidence:
                    lines.append(f"- {evidence.label}: {evidence.detail} ({evidence.source})")
                lines.append("")

    return "\n".join(lines).rstrip() + "\n"


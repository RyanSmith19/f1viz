from statistics import fmean

from f1viz.models.comparison import DriverComparisonFacts, DriverLapSummary
from f1viz.models.race_session import DriverInfo, LapInfo, RaceSession


class DriverComparisonService:
    """Build conservative comparison facts for any two drivers."""

    def compare(self, session: RaceSession, first: str, second: str) -> DriverComparisonFacts:
        first_driver = _find_driver(session, first)
        second_driver = _find_driver(session, second)
        first_summary = _summarize_driver_laps(
            first_driver,
            session.laps_for_driver(first_driver.driver_number),
        )
        second_summary = _summarize_driver_laps(
            second_driver,
            session.laps_for_driver(second_driver.driver_number),
        )

        return DriverComparisonFacts(
            first=first_summary,
            second=second_summary,
            best_lap_delta_seconds=_delta(
                first_summary.best_lap_duration,
                second_summary.best_lap_duration,
            ),
            average_lap_delta_seconds=_delta(
                first_summary.average_lap_duration,
                second_summary.average_lap_duration,
            ),
        )


def _find_driver(session: RaceSession, token: str) -> DriverInfo:
    if token.isdigit() and int(token) in session.drivers:
        return session.drivers[int(token)]

    driver = session.driver_by_acronym(token)
    if driver:
        return driver

    raise LookupError(f"No driver found for {token}")


def _summarize_driver_laps(driver: DriverInfo, laps: list[LapInfo]) -> DriverLapSummary:
    durations = [lap.lap_duration for lap in laps if lap.lap_duration is not None]
    return DriverLapSummary(
        driver_number=driver.driver_number,
        acronym=driver.acronym,
        lap_count=len(laps),
        best_lap_duration=min(durations) if durations else None,
        average_lap_duration=fmean(durations) if durations else None,
    )


def _delta(first: float | None, second: float | None) -> float | None:
    if first is None or second is None:
        return None
    return round(second - first, 3)


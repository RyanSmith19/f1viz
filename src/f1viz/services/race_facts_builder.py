from collections import Counter

from f1viz.models.race_facts import DriverRaceFacts, RaceFacts
from f1viz.models.race_session import RaceSession


class RaceFactsBuilder:
    """Build factual, non-interpretive summaries from a normalized race session."""

    def build(self, session: RaceSession) -> RaceFacts:
        return RaceFacts(
            driver_count=len(session.drivers),
            lap_count=len(session.laps),
            stint_count=len(session.stints),
            timeline_record_count=len(session.timeline),
            timeline_category_counts=dict(
                Counter(record.category for record in session.timeline)
            ),
            drivers={
                driver_number: DriverRaceFacts(
                    driver_number=driver_number,
                    acronym=driver.acronym,
                    lap_count=len(session.laps_for_driver(driver_number)),
                    stint_count=len(session.stints_for_driver(driver_number)),
                    timeline_record_count=len(session.timeline_for_driver(driver_number)),
                )
                for driver_number, driver in session.drivers.items()
            },
        )


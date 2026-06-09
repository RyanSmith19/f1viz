from datetime import UTC, datetime
from typing import Any

from f1viz.models.race_session import DriverInfo, LapInfo, RaceSession, StintInfo, TimelineRecord
from f1viz.models.session_data import RawSessionData
from f1viz.openf1 import OpenF1Endpoint

TIMESTAMPED_ENDPOINTS: tuple[OpenF1Endpoint, ...] = (
    OpenF1Endpoint.POSITION,
    OpenF1Endpoint.INTERVALS,
    OpenF1Endpoint.PIT,
    OpenF1Endpoint.RACE_CONTROL,
    OpenF1Endpoint.OVERTAKES,
)


class RaceSessionBuilder:
    """Build normalized race-session structures from raw OpenF1 endpoint records."""

    def build(self, data: RawSessionData) -> RaceSession:
        started_at = data.session.date_start or _earliest_timestamp(data)
        drivers = _build_drivers(data.get(OpenF1Endpoint.DRIVERS))
        laps = _build_laps(data.get(OpenF1Endpoint.LAPS))
        stints = _build_stints(data.get(OpenF1Endpoint.STINTS))
        timeline = _build_timeline(data=data, started_at=started_at)

        return RaceSession(
            meeting=data.meeting,
            session=data.session,
            started_at=started_at,
            drivers=drivers,
            laps=laps,
            stints=stints,
            timeline=timeline,
        )


def _build_drivers(rows: list[dict[str, Any]]) -> dict[int, DriverInfo]:
    drivers: dict[int, DriverInfo] = {}
    for row in rows:
        driver_number = int(row["driver_number"])
        drivers[driver_number] = DriverInfo(
            driver_number=driver_number,
            acronym=str(row.get("name_acronym") or driver_number),
            full_name=row.get("full_name"),
            team_name=row.get("team_name"),
        )
    return drivers


def _build_laps(rows: list[dict[str, Any]]) -> list[LapInfo]:
    laps = [
        LapInfo(
            driver_number=int(row["driver_number"]),
            lap_number=int(row["lap_number"]),
            lap_duration=row.get("lap_duration"),
            raw=row,
        )
        for row in rows
        if "driver_number" in row and "lap_number" in row
    ]
    return sorted(laps, key=lambda lap: (lap.driver_number, lap.lap_number))


def _build_stints(rows: list[dict[str, Any]]) -> list[StintInfo]:
    stints = [
        StintInfo(
            driver_number=int(row["driver_number"]),
            stint_number=int(row.get("stint_number") or row.get("stint") or 0),
            compound=row.get("compound"),
            lap_start=row.get("lap_start"),
            lap_end=row.get("lap_end"),
            raw=row,
        )
        for row in rows
        if "driver_number" in row
    ]
    return sorted(stints, key=lambda stint: (stint.driver_number, stint.stint_number))


def _build_timeline(data: RawSessionData, started_at: datetime) -> list[TimelineRecord]:
    records: list[TimelineRecord] = []
    for endpoint in TIMESTAMPED_ENDPOINTS:
        for row in data.get(endpoint):
            if "date" not in row:
                continue
            source_time = _parse_datetime(row["date"])
            records.append(
                TimelineRecord(
                    elapsed_seconds=(source_time - started_at).total_seconds(),
                    endpoint=endpoint,
                    driver_number=row.get("driver_number"),
                    category=_category_for(endpoint, row),
                    summary=_summary_for(endpoint, row),
                    source_time=source_time,
                    raw=row,
                )
            )
    return sorted(records, key=lambda record: record.elapsed_seconds)


def _earliest_timestamp(data: RawSessionData) -> datetime:
    timestamps = [
        _parse_datetime(row["date"])
        for endpoint in TIMESTAMPED_ENDPOINTS
        for row in data.get(endpoint)
        if "date" in row
    ]
    if not timestamps:
        raise ValueError("Cannot infer session start without session.date_start or dated records")
    return min(timestamps)


def _parse_datetime(value: str | datetime) -> datetime:
    if isinstance(value, datetime):
        parsed = value
    else:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))

    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def _category_for(endpoint: OpenF1Endpoint, row: dict[str, Any]) -> str:
    if endpoint == OpenF1Endpoint.RACE_CONTROL:
        return str(row.get("category") or "race_control").lower()
    return endpoint.value


def _summary_for(endpoint: OpenF1Endpoint, row: dict[str, Any]) -> str:
    if endpoint == OpenF1Endpoint.RACE_CONTROL:
        return str(row.get("message") or "Race control event")
    if endpoint == OpenF1Endpoint.POSITION:
        return f"Driver {row.get('driver_number')} position {row.get('position')}"
    if endpoint == OpenF1Endpoint.INTERVALS:
        return f"Driver {row.get('driver_number')} interval update"
    if endpoint == OpenF1Endpoint.PIT:
        return f"Driver {row.get('driver_number')} pit event"
    if endpoint == OpenF1Endpoint.OVERTAKES:
        return "Overtake event"
    return endpoint.value

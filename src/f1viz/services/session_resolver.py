from dataclasses import dataclass

from f1viz.models.openf1 import Meeting, Session


@dataclass(frozen=True)
class ResolvedSession:
    meeting: Meeting
    session: Session


class SessionResolver:
    """Resolve a user-facing race weekend/session selection from OpenF1 records."""

    def resolve(
        self,
        *,
        meetings: list[dict],
        sessions: list[dict],
        year: int,
        grand_prix: str,
        session_name: str = "Race",
    ) -> ResolvedSession:
        meeting = self._find_meeting(meetings=meetings, year=year, grand_prix=grand_prix)
        session = self._find_session(
            sessions=sessions,
            meeting_key=meeting.meeting_key,
            session_name=session_name,
        )
        return ResolvedSession(meeting=meeting, session=session)

    def _find_meeting(self, *, meetings: list[dict], year: int, grand_prix: str) -> Meeting:
        normalized_gp = _normalize(grand_prix)
        candidates = [Meeting.model_validate(item) for item in meetings]

        for meeting in candidates:
            searchable = " ".join(
                value
                for value in [
                    meeting.meeting_name,
                    meeting.country_name or "",
                    meeting.location or "",
                ]
                if value
            )
            if meeting.year == year and normalized_gp in _normalize(searchable):
                return meeting

        raise LookupError(f"No meeting found for {year} {grand_prix}")

    def _find_session(
        self,
        *,
        sessions: list[dict],
        meeting_key: int,
        session_name: str,
    ) -> Session:
        normalized_session = _normalize(session_name)
        candidates = [Session.model_validate(item) for item in sessions]

        for session in candidates:
            session_matches = _normalize(session.session_name) == normalized_session
            if session.meeting_key == meeting_key and session_matches:
                return session

        raise LookupError(f"No {session_name} session found for meeting {meeting_key}")


def _normalize(value: str) -> str:
    return "".join(character.lower() for character in value if character.isalnum())

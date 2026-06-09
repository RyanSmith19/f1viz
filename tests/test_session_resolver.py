from f1viz.services.session_resolver import SessionResolver


def test_session_resolver_matches_grand_prix_by_name() -> None:
    resolver = SessionResolver()

    resolved = resolver.resolve(
        meetings=[
            {
                "meeting_key": 1254,
                "year": 2025,
                "meeting_name": "Monaco Grand Prix",
                "country_name": "Monaco",
                "location": "Monte Carlo",
            }
        ],
        sessions=[
            {
                "session_key": 9991,
                "meeting_key": 1254,
                "session_name": "Race",
                "session_type": "Race",
                "year": 2025,
            }
        ],
        year=2025,
        grand_prix="monaco",
    )

    assert resolved.meeting.meeting_key == 1254
    assert resolved.session.session_key == 9991


def test_session_resolver_raises_for_missing_session() -> None:
    resolver = SessionResolver()

    try:
        resolver.resolve(
            meetings=[
                {
                    "meeting_key": 1254,
                    "year": 2025,
                    "meeting_name": "Monaco Grand Prix",
                }
            ],
            sessions=[],
            year=2025,
            grand_prix="monaco",
        )
    except LookupError as exc:
        assert "No Race session" in str(exc)
    else:
        raise AssertionError("Expected LookupError for missing race session")


import httpx

from f1viz.openf1 import OpenF1Client, OpenF1Endpoint


def test_openf1_client_builds_endpoint_url_and_params() -> None:
    seen_request: httpx.Request | None = None

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal seen_request
        seen_request = request
        return httpx.Response(200, json=[{"session_key": 1234}])

    transport = httpx.MockTransport(handler)
    http_client = httpx.Client(transport=transport)
    client = OpenF1Client(base_url="https://example.test/v1/", http_client=http_client)

    payload = client.get(OpenF1Endpoint.SESSIONS, {"year": 2025, "session_name": "Race"})

    assert payload == [{"session_key": 1234}]
    assert seen_request is not None
    assert str(seen_request.url) == "https://example.test/v1/sessions?year=2025&session_name=Race"


def test_openf1_client_rejects_non_list_payload() -> None:
    transport = httpx.MockTransport(lambda _request: httpx.Response(200, json={"bad": "shape"}))
    http_client = httpx.Client(transport=transport)
    client = OpenF1Client(base_url="https://example.test/v1", http_client=http_client)

    try:
        client.sessions(year=2025)
    except TypeError as exc:
        assert "returned dict" in str(exc)
    else:
        raise AssertionError("Expected TypeError for non-list OpenF1 payload")


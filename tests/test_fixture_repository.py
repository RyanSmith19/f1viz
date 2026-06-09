from f1viz.openf1 import OpenF1Endpoint
from f1viz.repositories.fixture_repository import FixtureRepository


def test_fixture_repository_round_trips_endpoint_payload(tmp_path) -> None:
    repository = FixtureRepository(tmp_path)
    payload = [{"driver_number": 4, "name_acronym": "NOR"}]

    path = repository.save(OpenF1Endpoint.DRIVERS, "sample-drivers", payload)
    loaded = repository.load(OpenF1Endpoint.DRIVERS, "sample-drivers")

    assert path == tmp_path / "drivers" / "sample-drivers.json"
    assert loaded == payload


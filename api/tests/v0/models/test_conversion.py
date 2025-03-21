import pytest

from src.v0.models.objective import ObjectiveResponse
from src.v0.models.vertex import VertexResponse


@pytest.fixture
def metadata():
    return {
        "version": "v0",
        "uuid": "1",
        "timestamp": "1234",
        "date": "today",
        "T.id": "1",
        "T.label": "L",
    }


@pytest.fixture
def objective():
    return {
        "description": "an objective description",
        "tag": ["junk"],
        "index": "1234",
        "hierarchy": "fundamental",
    }


def test_convert_api_payload_to_response_success(metadata, objective):
    body = {**objective, **metadata}
    vertex = VertexResponse.model_validate(body)
    result = ObjectiveResponse.convert_api_payload_to_response(vertex)
    assert result.description == "an objective description"
    assert isinstance(result, ObjectiveResponse)


def test_convert_api_payload_to_response_fail(metadata):
    body = {**{"objective": None}, **metadata}
    vertex = VertexResponse.model_validate(body)
    with pytest.raises(Exception) as exc:
        ObjectiveResponse.convert_api_payload_to_response(vertex)
    assert "Cannot validate the API payload into a data model response" in str(exc.value)


def test_convert_list_api_payloads_to_responses_success(metadata, objective):
    body = {**objective, **metadata}
    vertices = [VertexResponse.model_validate(body)]
    result = ObjectiveResponse.convert_list_api_payloads_to_responses(vertices)
    assert result[0].description == "an objective description"
    assert isinstance(result[0], ObjectiveResponse)


def test_convert_list_api_payloads_to_responses_fail(metadata, objective):
    body = {**{"objective": None}, **metadata}
    vertices = [VertexResponse.model_validate(body)]
    with pytest.raises(Exception) as exc:
        ObjectiveResponse.convert_list_api_payloads_to_responses(vertices)
    assert "Cannot validate the API payload into a data model response" in str(exc.value)

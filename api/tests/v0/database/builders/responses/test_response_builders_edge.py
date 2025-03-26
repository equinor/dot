from src.v0.database.builders.responses.gremlin_responses_edge import (
    GremlinResponseBuilderEdge,
)


def test_edge_response_builder_parse_edge():
    assert GremlinResponseBuilderEdge()._parse_edge("e[A][B-C->D]") == {
        "id": "A",
        "label": "C",
        "outV": "B",
        "inV": "D",
        "uuid": "A",
    }


def test_edge_response_builder_parse_edge_dictionary():
    assert GremlinResponseBuilderEdge()._parse_edge(
        {
            "id": "A",
            "label": "C",
            "outV": "B",
            "inV": "D",
            "uuid": "A",
        }
    ) == {
        "id": "A",
        "label": "C",
        "outV": "B",
        "inV": "D",
        "uuid": "A",
    }


def test_edge_response_builder_item():
    assert GremlinResponseBuilderEdge().build_item(["e[A][B-C->D]"]).model_dump() == {
        "id": "A",
        "label": "c",
        "outV": "B",
        "inV": "D",
        "uuid": "A",
        "version": "v0",
    }


def test_edge_response_builder_list():
    assert GremlinResponseBuilderEdge().build_list(["e[A][B-C->D]"])[0].model_dump() == {
        "id": "A",
        "label": "c",
        "outV": "B",
        "inV": "D",
        "uuid": "A",
        "version": "v0",
    }


def test_edge_response_build_none():
    assert GremlinResponseBuilderEdge().build_none() is None

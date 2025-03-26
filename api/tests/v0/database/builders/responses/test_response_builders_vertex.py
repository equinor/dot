import pytest

from src.v0.database.builders.responses.gremlin_responses_vertex import (
    FieldParserVertex,
    GremlinResponseBuilderVertex,
)


def test_FieldParser():
    assert FieldParserVertex().id("an id") == "an id"
    assert FieldParserVertex().label("a label") == "a label"
    assert FieldParserVertex().string(["a string"]) == "a string"
    assert FieldParserVertex().list(None) is None
    assert FieldParserVertex().list("") is None
    assert FieldParserVertex().list([]) is None
    assert FieldParserVertex().list(['["yes", "no"]']) == ["yes", "no"]
    assert (
        FieldParserVertex().probability(None) is None
    )  # cannot be as default_probability is set by default - legacy
    assert FieldParserVertex().probability([None]) is None
    assert FieldParserVertex().probability([""]) is None
    assert (
        FieldParserVertex().probability(["null"]) is None
    )  # cannot be as default_probability is set by default - legacy
    # assert VertexFieldParser().\
    #   probability([default_probability.model_dump_json()]) == \
    #   default_probability.model_dump()
    with pytest.raises(Exception) as exc:
        FieldParserVertex().probability("a string")
    assert str(exc.value) == "Probability in DataBase is not in a ProbabilityData format"
    with pytest.raises(Exception) as exc:
        FieldParserVertex().id(["an id"])
    assert str(exc.value) == "The id should be a string"
    with pytest.raises(Exception) as exc:
        FieldParserVertex().label(["a label"])
    assert str(exc.value) == "The label should be a string"
    assert FieldParserVertex().comments(None) is None
    assert FieldParserVertex().comments(["null"]) is None
    assert FieldParserVertex().comments([""]) is None
    with pytest.raises(Exception) as exc:
        FieldParserVertex().comments("a string")
    assert str(exc.value) == "The data should be a list"
    with pytest.raises(Exception) as exc:
        FieldParserVertex().comments(['["a comment"]'])
    assert str(exc.value) == (
        "Comment in DataBase is not in a CommentData format: a comment"
    )


def test_vertex_response_build_item():
    data = [
        {
            "tag": ['["a tag"]'],
            "alternatives": ['["red", "green", "blue"]'],
            "description": ["John Doe"],
            "probabilities": [
                (
                    '{"dtype": "DiscreteUnconditionalProbability",'
                    '"probability_function": [[1.0]],'
                    '"variables": {"variable": ["outcome"]}}'
                )
            ],
            "comments": ['[{"comment": "a comment", "author": "an author"}]'],
            "timestamp": ["1622477127.0"],
            "date": ["2024-06-01 00:00:00"],
            "uuid": ["134a1f4a-2c11-46a2-b5cf-8498ef99aa08"],
            "ids": ["test"],
            "T.id": "134a1f4a-2c11-46a2-b5cf-8498ef99aa08",
            "T.label": "vertex",
            "id": "134a1f4a-2c11-46a2-b5cf-8498ef99aa08",
            "version": ["v0"],
        }
    ]
    assert GremlinResponseBuilderVertex().build_item(data).model_dump() == {
        "tag": ["a tag"],
        "alternatives": ["red", "green", "blue"],
        "description": "John Doe",
        "probabilities": {
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [[1.0]],
            "variables": {"variable": ["outcome"]},
        },
        "comments": [{"comment": "a comment", "author": "an author"}],
        "uuid": "134a1f4a-2c11-46a2-b5cf-8498ef99aa08",
        "timestamp": "1622477127.0",
        "date": "2024-06-01 00:00:00",
        "id": "134a1f4a-2c11-46a2-b5cf-8498ef99aa08",
        "label": "vertex",
        "ids": "test",
        "version": "v0",
    }

def test_vertex_response_build_item_without_T_variables():
    data = [
        {
            "tag": ['["a tag"]'],
            "alternatives": ['["red", "green", "blue"]'],
            "description": ["John Doe"],
            "probabilities": [
                (
                    '{"dtype": "DiscreteUnconditionalProbability",'
                    '"probability_function": [[1.0]],'
                    '"variables": {"variable": ["outcome"]}}'
                )
            ],
            "comments": ['[{"comment": "a comment", "author": "an author"}]'],
            "timestamp": ["1622477127.0"],
            "date": ["2024-06-01 00:00:00"],
            "uuid": ["134a1f4a-2c11-46a2-b5cf-8498ef99aa08"],
            "ids": ["test"],
            "label": "vertex",
            "id": "134a1f4a-2c11-46a2-b5cf-8498ef99aa08",
            "version": ["v0"],
        }
    ]
    assert GremlinResponseBuilderVertex().build_item(data).model_dump() == {
        "tag": ["a tag"],
        "alternatives": ["red", "green", "blue"],
        "description": "John Doe",
        "probabilities": {
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [[1.0]],
            "variables": {"variable": ["outcome"]},
        },
        "comments": [{"comment": "a comment", "author": "an author"}],
        "uuid": "134a1f4a-2c11-46a2-b5cf-8498ef99aa08",
        "timestamp": "1622477127.0",
        "date": "2024-06-01 00:00:00",
        "id": "134a1f4a-2c11-46a2-b5cf-8498ef99aa08",
        "label": "vertex",
        "ids": "test",
        "version": "v0",
    }


def test_vertex_response_build_item_fail():
    data = [
        {
            "not_working_field": "should be a list",
        }
    ]
    with pytest.raises(Exception) as exc:
        GremlinResponseBuilderVertex().build_item(data)
    assert str(exc.value) == "Parser for field 'not_working_field' is not defined"


def test_vertex_response_build_list():
    data = [
        {
            "tag": ['["a tag"]'],
            "alternatives": ['["red", "green", "blue"]'],
            "description": ["John Doe"],
            "probabilities": [
                (
                    '{"dtype": "DiscreteUnconditionalProbability",'
                    '"probability_function": [[1.0]],'
                    '"variables": {"variable": ["outcome"]}}'
                )
            ],
            "timestamp": ["1622477127.0"],
            "date": ["2024-06-01 00:00:00"],
            "uuid": ["134a1f4a-2c11-46a2-b5cf-8498ef99aa08"],
            "ids": ["test"],
            "T.id": "134a1f4a-2c11-46a2-b5cf-8498ef99aa08",
            "T.label": "vertex",
            "version": ["v0"],
        }
    ]
    assert GremlinResponseBuilderVertex().build_list(data)[0].model_dump() == {
        "tag": ["a tag"],
        "alternatives": ["red", "green", "blue"],
        "description": "John Doe",
        "probabilities": {
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [[1.0]],
            "variables": {"variable": ["outcome"]},
        },
        "uuid": "134a1f4a-2c11-46a2-b5cf-8498ef99aa08",
        "timestamp": "1622477127.0",
        "date": "2024-06-01 00:00:00",
        "id": "134a1f4a-2c11-46a2-b5cf-8498ef99aa08",
        "label": "vertex",
        "ids": "test",
        "version": "v0",
    }


def test_vertex_response_build_none():
    assert GremlinResponseBuilderVertex().build_none() is None

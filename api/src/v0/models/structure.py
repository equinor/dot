from ... import DOTModel
from .edge import EdgeResponse
from .issue import IssueResponse, ProbabilityData

# TODO: ID model
# TODO: DT model


class InfluenceDiagramResponse(DOTModel):
    nodes: list[IssueResponse]
    arcs: list[EdgeResponse]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nodes": [
                        {
                            "tag": "subsurface",
                            "category": "uncertainty",
                            "index": "0",
                            "shortname": "thelitissue",
                            "description": "this is an issue to call yours",
                            "keyUncertainty": "true",
                            "decisionType": "tactical",
                            "alternatives": "[do or do not, there is no try]",
                            "probabilities": "[0.3, 0.7]",
                            "influenceNodeUUID": "123",
                            "uuid": "98d186e8-a506-4819-b040-dc0405a464c2",
                            "timestamp": 1710400325.0692892,
                            "date": "2024-03-14T07:12:05.069295",
                            "ids": "test",
                        },
                        {
                            "tag": "subsurface",
                            "category": "decision",
                            "index": "0",
                            "shortname": "thelitissue",
                            "description": "this is an issue to call yours",
                            "keyUncertainty": "true",
                            "decisionType": "tactical",
                            "alternatives": "[do or do not, there is no try]",
                            "probabilities": "[0.3, 0.7]",
                            "influenceNodeUUID": "123",
                            "uuid": "8e729eb3-f47d-4380-99d8-ed823376dc86",
                            "timestamp": 1710400330.6278934,
                            "date": "2024-03-14T07:12:10.627895",
                            "ids": "test",
                        },
                        {
                            "tag": "subsurface",
                            "category": "decision",
                            "index": "0",
                            "shortname": "thelitissue",
                            "description": "this is an issue to call yours",
                            "keyUncertainty": "true",
                            "decisionType": "tactical",
                            "alternatives": "[do or do not, there is no try]",
                            "probabilities": "[0.3, 0.7]",
                            "influenceNodeUUID": "123",
                            "uuid": "ed58b7b1-ff91-4886-9311-7b1787d76cb1",
                            "timestamp": 1710400330.0167134,
                            "date": "2024-03-14T07:12:10.016715",
                            "ids": "test",
                        },
                    ],
                    "arcs": [
                        {
                            "id": "3ed21afc-be76-4b14-be63-6d626e9fbb3c",
                            "outV": "ed58b7b1-ff91-4886-9311-7b1787d76cb1",
                            "inV": "8e729eb3-f47d-4380-99d8-ed823376dc86",
                            "uuid": "3ed21afc-be76-4b14-be63-6d626e9fbb3c",
                        },
                        {
                            "id": "1b32fd0d-7169-496e-9881-893b18f5f8cf",
                            "outV": "ed58b7b1-ff91-4886-9311-7b1787d76cb1",
                            "inV": "98d186e8-a506-4819-b040-dc0405a464c2",
                            "uuid": "1b32fd0d-7169-496e-9881-893b18f5f8cf",
                        },
                    ],
                }
            ]
        }
    }


class DecisionTreeNodeData(DOTModel):
    node_type: str
    description: str
    shortname: str
    uuid: str
    branch_name: str
    alternatives: list[str] | None = (
        None  # List[str]] #or list [str works at the moment]
    )
    probabilities: ProbabilityData | None = None
    utility: list[str] | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "node_type": "DecisionNode",
                    "name": "Joe can test the car",
                    "shortname": "Test",
                    "uuid": "ad651f50-22de-4f85-a560-bf5fb2d9f706",
                    "alternatives": ["Test", " no Test"],
                }
            ]
        }
    }


class DecisionTreeResponse(DOTModel):
    id: DecisionTreeNodeData
    children: list["DecisionTreeResponse"] | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": {
                        "node_type": "DecisionNode",
                        "name": "Joe can test the car",
                        "shortname": "Test",
                        "uuid": "ad651f50-22de-4f85-a560-bf5fb2d9f706",
                        "alternatives": ['"Test"', '" no Test"'],
                    },
                    "children": [
                        {
                            "id": {
                                "node_type": "UncertaintyNode",
                                "name": "The result of the test is currently unknown",
                                "shortname": "Test Result",
                                "uuid": "e0d590dc-b62f-4476-b8cc-aee672f29458",
                                "probabilities": {
                                    "dtype": "DiscreteUnconditionalProbability",
                                    "cpt": None,
                                },
                            },
                            "children": [
                                {
                                    "id": {
                                        "node_type": "UtilityNode",
                                        "name": "Utility",
                                        "shortname": "v",
                                        "uuid": "55d46d6b-9563-4fbc-80aa-8368a60d3e31",
                                        "utility": [],
                                    }
                                }
                            ],
                        }
                    ],
                }
            ]
        }
    }


DecisionTreeResponse.model_rebuild()

import pytest

from src.v0.models.issue import (
    DiscreteUnconditionalProbabilityData,
    DiscreteConditionalProbabilityData,
    DecisionData,
    UncertaintyData,
    ValueMetricData,
    CommentData,
    IssueCreate,
    IssueUpdate,
    none_probability_function,
    variables_probability_function_consistence,
    default_probability,
)


def test_reset_probability_function():
    variables = {'n1': ['s11', 's12'],
                 'n2': ['s21', 's22', 's23'],
                 'n3': ['s31', 's32']}
    target = [
        [None, None, None, None, None, None],
        [None, None, None, None, None, None]
        ]
    result = none_probability_function(variables)
    assert result == target


def test_variables_probability_function_consistence():
    variables = {'n1': ['s11', 's12'],
                 'n2': ['s21', 's22', 's23'],
                 'n3': ['s31', 's32']}
    probability_function = [
        [None, None, None, None, None, None],
        [None, None, None, None, None, None]
        ] 
    assert variables_probability_function_consistence(variables, probability_function)

    variables = {'n1': ['s11', 's12']}
    probability_function = [[None], [None]] 
    assert variables_probability_function_consistence(variables, probability_function)

    variables = {'n1': ['s11', 's12'],
                 'n2': ['s21', 's22', 's23']}
    probability_function = [
        [None, None, None, None, None, None],
        [None, None, None, None, None, None]
        ] 
    assert not variables_probability_function_consistence(variables, probability_function)


def test_DiscreteUnconditionalProbabilityData_success():
    probability = DiscreteUnconditionalProbabilityData(
        dtype = "DiscreteUnconditionalProbability",
        probability_function = [[0.3], [0.7]],
        variables = {"variable": ["state1", "state2"]},
    )
    
    assert probability.model_dump() == {
        "dtype": "DiscreteUnconditionalProbability",
        "probability_function": [[0.3], [0.7]],
        "variables": {"variable": ["state1", "state2"]},
    }

    probability.variables = {"variable": ["state1", "state2", "state3"]}
    assert probability.probability_function == [[None], [None], [None]]

    probability.variables = {"variable": ["state1", "state2"]}
    assert probability.probability_function == [[None], [None]]

    probability = DiscreteUnconditionalProbabilityData(
        dtype = "DiscreteUnconditionalProbability",
        probability_function = [[0.3], [0.7], [0.5]],
        variables = {"variable": ["state1", "state2"]},
    )
    assert probability.probability_function == [[None], [None]]


def test_DiscreteUnconditionalProbabilityData_2d_success():
    probability = DiscreteUnconditionalProbabilityData(
        dtype = "DiscreteUnconditionalProbability",
        probability_function = [[0.3, 0.1, 0.4], [0.7, 0.9, 0.6]],
        variables = {"v1": ["s11", "s12"], "v2": ["s12", "s22", "s32"]},
    )
    
    assert probability.model_dump() == {
        "dtype": "DiscreteUnconditionalProbability",
        "probability_function": [[0.3, 0.1, 0.4], [0.7, 0.9, 0.6]],
        "variables": {"v1": ["s11", "s12"], "v2": ["s12", "s22", "s32"]},
    }

    probability.variables = {"variable": ["state1", "state2", "state3"]}
    assert probability.probability_function == [[None], [None], [None]]


def test_DiscreteConditionalProbabilityData_success():
    probability = DiscreteConditionalProbabilityData(
        dtype = "DiscreteConditionalProbability",
        probability_function = [[0.3, 0.6], [0.7, 0.4]],
        conditioned_variables = {"variable": ["state1", "state2"]},
        conditioning_variables = {"parent": ["o1", "o2"]},
        parents_uuid = ["1"],
    )
    
    assert probability.model_dump() == {
        "dtype": "DiscreteConditionalProbability",
        "probability_function": [[0.3, 0.6], [0.7, 0.4]],
        "conditioned_variables": {"variable": ["state1", "state2"]},
        "conditioning_variables": {"parent": ["o1", "o2"]},
        "parents_uuid": ["1"]
    }

    probability.conditioned_variables = {"variable": ["state1", "state2", "state3"]}
    assert probability.probability_function == [[None, None], [None, None], [None, None]]

    probability.conditioned_variables = {"variable": ["state1", "state2"]}
    assert probability.probability_function == [[None, None], [None, None]]

    probability.conditioning_variables = {"name2": ["o1", "o2"]}
    assert probability.probability_function == [[None, None], [None, None]]

    probability = DiscreteConditionalProbabilityData(
        dtype = "DiscreteConditionalProbability",
        probability_function = [[0.3, 0.6, 0.6], [0.7, 0.4, 0.6]],
        conditioned_variables = {"variable": ["state1", "state2"]},
        conditioning_variables = {"parent": ["o1", "o2"]},
        parents_uuid = ["1"],
    )
    assert probability.probability_function == [[None, None], [None, None]]


def test_default_probability():
    assert default_probability({'shortname': 'x'}).model_dump() == {
        "dtype": "DiscreteUnconditionalProbability",
        "probability_function": [[None]],
        "variables": {"x": ["state1"]},        
    }


def test_UncertaintyData_None_success():
    uncertainty = UncertaintyData(
        probability=None,
        key="True",
        source="out of the blue"
    )    
    uncertainty.model_dump() == {
        "probability": None,
        "key": "True",
        "source": "out of the blue",
        }

    assert uncertainty.probability is None
        

def test_UncertaintyData_unconditional_success():
    uncertainty = UncertaintyData(
        probability={
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [[0.3], [0.7]],
            "variables": {"variable": ["state1", "state2"]},
        },
        key="True",
        source="out of the blue"
    )    
    uncertainty.model_dump() == {
        "probability": {
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [[0.3], [0.7]],
            "variables": {"variable": ["state1", "state2"]},
            },
        "key": "True",
        "source": "out of the blue",
        }

    assert isinstance(uncertainty.probability, DiscreteUnconditionalProbabilityData)
        

def test_UncertaintyData_conditional_success():
    uncertainty = UncertaintyData(
        probability={
            "dtype": "DiscreteConditionalProbability",
            "probability_function": [[0.3, 0.6], [0.7, 0.4]],
            "conditioned_variables": {"variable": ["state1", "state2"]},
            "conditioning_variables": {"parent": ["o1", "o2"]},
            "parents_uuid": ["1"]
        },
        key="False",
        source="out of the blue"
    )    
    uncertainty.model_dump() == {
        "probability": {            
            "dtype": "DiscreteConditionalProbability",
            "probability_function": [[0.3, 0.6], [0.7, 0.4]],
            "conditioned_variables": {"variable": ["state1", "state2"]},
            "conditioning_variables": {"parent": ["o1", "o2"]},
            "parents_uuid": ["1"]
            },
        "key": "False",
        "source": "out of the blue",
        }

    assert isinstance(uncertainty.probability, DiscreteConditionalProbabilityData)


def test_DecisionData_success():
    decision_data = DecisionData()
    assert decision_data.states is None
    assert decision_data.decision_type is None

    decision_data = DecisionData(states=["yes", "no"], decision_type="Focus")
    assert decision_data.states == ["yes", "no"]
    assert decision_data.decision_type == "Focus"


def test_DecisionData_fail():
    with pytest.raises(Exception) as exc:
        DecisionData(decision_type="not defined")
    assert (
        "1 validation error for DecisionData\ndecision_type\n  "
        "Input should be 'Focus', 'Tactical' or 'Strategic' "
        "[type=literal_error, input_value='not defined', input_type=str]\n    "
        "For further information visit https://errors.pydantic.dev/2.10/v/literal_error"
        ) in str(exc.value)


def test_ValueMetricData_success():
    assert ValueMetricData().model_dump() == {
        "cost_function": None,
        "weigth": None,
    }
    
    assert ValueMetricData(
        cost_function="minimize_expected_utility",
        weigth=0.5,
    ).model_dump() == {
        "cost_function": "minimize_expected_utility",
        "weigth": 0.5,
    }


def test_CommentData_success():
    assert CommentData(
        comment="a comment",
        author="an author",
    ).model_dump() == {
        "comment": "a comment",
        "author": "an author",
    }


def test_CommentData_fail():
    with pytest.raises(Exception) as exc:
        CommentData(
            comment="a comment",
        )
    assert (
        "1 validation error for CommentData\nauthor\n  Field required [type=missing, "
        "input_value={'comment': 'a comment'}, input_type=dict]\n    For further "
        "information visit https://errors.pydantic.dev/2.10/v/missing"
    ) in str(exc.value)


def test_IssueCreate_default():
    issue = IssueCreate(description="a description")
    assert issue.model_dump() == {
        "tag": None,
        "category": None,
        "index": None,
        "shortname": None,
        "description": "a description",
        "uncertainty": None,
        "decision": None,
        "value_metric": None,
        "boundary": None,
        "comments": None,
    }


def test_IssueCreate_update_states():
    issue = IssueCreate(description="a description")
    issue.uncertainty = UncertaintyData(
        probability={
            "dtype": "DiscreteConditionalProbability",
            "probability_function": [[0.3, 0.6], [0.7, 0.4]],
            "conditioned_variables": {"variable": ["state1", "state2"]},
            "conditioning_variables": {"parent": ["o1", "o2"]},
            "parents_uuid": ["1"]
        },
        key="False",
        source="out of the blue"
    )
    issue.uncertainty.probability.conditioned_variables = {"variable": ["ou1", "out2"]}
    assert issue.model_dump() == {
        "tag": None,
        "category": None,
        "index": None,
        "shortname": None,
        "description": "a description",
        "uncertainty": {
        "probability": {
            "dtype": "DiscreteConditionalProbability",
            "probability_function": [[0.3, 0.6], [0.7, 0.4]],
            "conditioned_variables": {"variable": ["ou1", "out2"]},
            "conditioning_variables": {"parent": ["o1", "o2"]},
            "parents_uuid": ["1"]
            },
        "key": "False",
        "source": "out of the blue",
        },
        "decision": None,
        "value_metric": None,
        "boundary": None,
        "comments": None,
    }


def test_IssueCreate_set_default_probability():
    issue = IssueCreate(
        description="a description",
        category="Uncertainty"
        )
    assert issue.model_dump() == {
        "tag": None,
        "category": "Uncertainty",
        "index": None,
        "shortname": None,
        "description": "a description",
        "uncertainty": {
            "probability": {
                'dtype': 'DiscreteUnconditionalProbability',
                'probability_function': [[None]],
                'variables': {'variable': ['state1']}
                },
            "key": "False",
            "source": ""
            },
        "decision": None,
        "value_metric": None,
        "boundary": None,
        "comments": None,
    }

    issue = IssueCreate(
        description="a description",
        category="Uncertainty",
        uncertainty={
            "probability": {
                'dtype': 'DiscreteUnconditionalProbability',
                'probability_function': [[0.3], [0.7]],
                'variables': {'variable': ['s1', 's2']}
                },
            "key": "False",
            "source": ""
            }
        )
    assert issue.model_dump() == {
        "tag": None,
        "category": "Uncertainty",
        "index": None,
        "shortname": None,
        "description": "a description",
        "uncertainty": {
            "probability": {
                'dtype': 'DiscreteUnconditionalProbability',
                'probability_function': [[0.3], [0.7]],
                'variables': {'variable': ['s1', 's2']}
                },
            "key": "False",
            "source": ""
            },
        "decision": None,
        "value_metric": None,
        "boundary": None,
        "comments": None,
    }


def test_IssueCreate_set_default_decision():
    issue = IssueCreate(
        description="a description",
        category="Decision"
        )
    assert issue.model_dump() == {
        "tag": None,
        "category": "Decision",
        "index": None,
        "shortname": None,
        "description": "a description",
        "uncertainty": None,
        "decision": {
            "states": None,
            "decision_type": None
        },
        "value_metric": None,
        "boundary": None,
        "comments": None,
    }


def test_IssueCreate_set_default_value_metric():
    issue = IssueCreate(
        description="a description",
        category="Value Metric"
        )
    assert issue.model_dump() == {
        "tag": None,
        "category": "Value Metric",
        "index": None,
        "shortname": None,
        "description": "a description",
        "uncertainty": None,
        "decision": None,
        "value_metric": {
            "cost_function": None,
            "weigth": None
        },
        "boundary": None,
        "comments": None,
    }    


def test_IssueUpdate_default():
    issue = IssueUpdate(description="a description")
    assert issue.model_dump() == {
        "tag": None,
        "category": None,
        "index": None,
        "shortname": None,
        "description": "a description",
        "uncertainty": None,
        "decision": None,
        "value_metric": None,
        "boundary": None,
        "comments": None,
    }


def test_IssueUpdate_update_states():
    issue = IssueUpdate(description="a description")
    issue.uncertainty = UncertaintyData(
        probability={
            "dtype": "DiscreteConditionalProbability",
            "probability_function": [[0.3, 0.6], [0.7, 0.4]],
            "conditioned_variables": {"variable": ["state1", "state2"]},
            "conditioning_variables": {"parent": ["o1", "o2"]},
            "parents_uuid": ["1"]
        },
        key="False",
        source="out of the blue"
    )
    issue.uncertainty.probability.conditioned_variables = {"variable": ["ou1", "out2"]}
    assert issue.model_dump() == {
        "tag": None,
        "category": None,
        "index": None,
        "shortname": None,
        "description": "a description",
        "uncertainty": {
        "probability": {
            "dtype": "DiscreteConditionalProbability",
            "probability_function": [[0.3, 0.6], [0.7, 0.4]],
            "conditioned_variables": {"variable": ["ou1", "out2"]},
            "conditioning_variables": {"parent": ["o1", "o2"]},
            "parents_uuid": ["1"]
            },
        "key": "False",
        "source": "out of the blue",
        },
        "decision": None,
        "value_metric": None,
        "boundary": None,
        "comments": None,
    }


def test_IssueUpdate_set_default_probability():
    issue = IssueUpdate(
        description="a description",
        category="Uncertainty"
        )
    assert issue.model_dump() == {
        "tag": None,
        "category": "Uncertainty",
        "index": None,
        "shortname": None,
        "description": "a description",
        "uncertainty": {
            "probability": {
                'dtype': 'DiscreteUnconditionalProbability',
                'probability_function': [[None]],
                'variables': {'variable': ['state1']}
                },
            "key": "False",
            "source": ""
            },
        "decision": None,
        "value_metric": None,
        "boundary": None,
        "comments": None,
    }

    issue = IssueUpdate(
        description="a description",
        category="Uncertainty",
        uncertainty={
            "probability": {
                'dtype': 'DiscreteUnconditionalProbability',
                'probability_function': [[0.3], [0.7]],
                'variables': {'variable': ['s1', 's2']}
                },
            "key": "False",
            "source": ""
            }
        )
    assert issue.model_dump() == {
        "tag": None,
        "category": "Uncertainty",
        "index": None,
        "shortname": None,
        "description": "a description",
        "uncertainty": {
            "probability": {
                'dtype': 'DiscreteUnconditionalProbability',
                'probability_function': [[0.3], [0.7]],
                'variables': {'variable': ['s1', 's2']}
                },
            "key": "False",
            "source": ""
            },
        "decision": None,
        "value_metric": None,
        "boundary": None,
        "comments": None,
    }


def test_IssueUpdate_set_default_decision():
    issue = IssueUpdate(
        description="a description",
        category="Decision"
        )
    assert issue.model_dump() == {
        "tag": None,
        "category": "Decision",
        "index": None,
        "shortname": None,
        "description": "a description",
        "uncertainty": None,
        "decision": {
            "states": None,
            "decision_type": None
        },
        "value_metric": None,
        "boundary": None,
        "comments": None,
    }


def test_IssueUpdate_set_default_value_metric():
    issue = IssueUpdate(
        description="a description",
        category="Value Metric"
        )
    assert issue.model_dump() == {
        "tag": None,
        "category": "Value Metric",
        "index": None,
        "shortname": None,
        "description": "a description",
        "uncertainty": None,
        "decision": None,
        "value_metric": {
            "cost_function": None,
            "weigth": None
        },
        "boundary": None,
        "comments": None,
    }        
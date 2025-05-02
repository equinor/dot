import pytest

from src.v0.services.reporting_utils import markdown_issue


@pytest.fixture
def issue_data():
    return [
        {"category": "Fact", "description": "Fact 1", "shortname": "F1", "boundary": "on", "keyUncertainty": "", "decisionType": "", "alternatives": []},
        {"category": "Fact", "description": "Fact 2", "shortname": "F2", "boundary": "", "keyUncertainty": "", "decisionType": "", "alternatives": []},
        {"category": "Value Metric", "description": "Value 1", "shortname": "V1", "boundary": "on", "keyUncertainty": "", "decisionType": "", "alternatives": []},
        {"category": "Value Metric", "description": "Value 2", "shortname": "V2", "boundary": "out", "keyUncertainty": "", "decisionType": "", "alternatives": []},
        {"category": "", "description": "Nada 1", "shortname": "N1", "boundary": "", "keyUncertainty": "", "decisionType": "", "alternatives": []},
        {"category": "", "description": "Nada 2", "shortname": "N2", "boundary": "", "keyUncertainty": "", "decisionType": "", "alternatives": []},
        {"category": "Decision", "description": "Decision 1", "shortname": "D1", "boundary": "on", "keyUncertainty": "", "decisionType": "Focus", "alternatives": ["yes", "no"]},
        {"category": "Decision", "description": "Decision 2", "shortname": "D2", "boundary": "out", "keyUncertainty": "", "decisionType": "", "alternatives": ["yes", "no"]},
        {"category": "Decision", "description": "Decision 3", "shortname": "D3", "boundary": "in", "keyUncertainty": "", "decisionType": "", "alternatives": ["yes", "no"]},
        {"category": "Decision", "description": "Decision 4", "shortname": "D4", "boundary": "in", "keyUncertainty": "", "decisionType": "", "alternatives": []},
        {"category": "Decision", "description": "Decision 5", "shortname": "D5", "boundary": "in", "keyUncertainty": "", "decisionType": "", "alternatives": []},
        {"category": "Uncertainty", "description": "Uncertainty 1", "shortname": "U1", "boundary": "", "keyUncertainty": "", "decisionType": "", "alternatives": []},
        {"category": "Uncertainty", "description": "Uncertainty 2", "shortname": "U2", "boundary": "in", "keyUncertainty": "true", "decisionType": "", "alternatives": []},
        {"category": "Uncertainty", "description": "Uncertainty 3", "shortname": "U3", "boundary": "in", "keyUncertainty": "", "decisionType": "", "alternatives": []}
    ]


def test_group_issues(issue_data):
    assert markdown_issue.group_issues(issue_data) == [
        {"category": "Fact", "description": "Fact 1", "shortname": "F1", "boundary": "on", "keyUncertainty": "Unset", "decisionType": "Unset", "alternatives": []},
        {"category": "Fact", "description": "Fact 2", "shortname": "F2", "boundary": "Unset", "keyUncertainty": "Unset", "decisionType": "Unset", "alternatives": []},
        {"category": "Decision", "description": "Decision 3", "shortname": "D3", "boundary": "in", "keyUncertainty": "Unset", "decisionType": "Unset", "alternatives": ["yes", "no"]},
        {"category": "Decision", "description": "Decision 4", "shortname": "D4", "boundary": "in", "keyUncertainty": "Unset", "decisionType": "Unset", "alternatives": []},
        {"category": "Decision", "description": "Decision 5", "shortname": "D5", "boundary": "in", "keyUncertainty": "Unset", "decisionType": "Unset", "alternatives": []},
        {"category": "Decision", "description": "Decision 1", "shortname": "D1", "boundary": "on", "keyUncertainty": "Unset", "decisionType": "Focus", "alternatives": ["yes", "no"]},
        {"category": "Decision", "description": "Decision 2", "shortname": "D2", "boundary": "out", "keyUncertainty": "Unset", "decisionType": "Unset", "alternatives": ["yes", "no"]},
        {"category": "Uncertainty", "description": "Uncertainty 2", "shortname": "U2", "boundary": "in", "keyUncertainty": "true", "decisionType": "Unset", "alternatives": []},
        {"category": "Uncertainty", "description": "Uncertainty 3", "shortname": "U3", "boundary": "in", "keyUncertainty": "Unset", "decisionType": "Unset", "alternatives": []},
        {"category": "Uncertainty", "description": "Uncertainty 1", "shortname": "U1", "boundary": "Unset", "keyUncertainty": "Unset", "decisionType": "Unset", "alternatives": []},
        {"category": "Value Metric", "description": "Value 1", "shortname": "V1", "boundary": "on", "keyUncertainty": "Unset", "decisionType": "Unset", "alternatives": []},
        {"category": "Value Metric", "description": "Value 2", "shortname": "V2", "boundary": "out", "keyUncertainty": "Unset", "decisionType": "Unset", "alternatives": []},
        {"category": "Uncategorized", "description": "Nada 1", "shortname": "N1", "boundary": "Unset", "keyUncertainty": "Unset", "decisionType": "Unset", "alternatives": []},
        {"category": "Uncategorized", "description": "Nada 2", "shortname": "N2", "boundary": "Unset", "keyUncertainty": "Unset", "decisionType": "Unset", "alternatives": []},
    ]
    

def test_clean_issues_facts(issue_data):
    grouped = markdown_issue.group_issues(issue_data)
    assert markdown_issue.clean_issues(grouped, "Fact", ["description", "shortname", "boundary"]) == [
        {"description": "Fact 1", "shortname": "F1", "boundary": "on"},
        {"description": "Fact 2", "shortname": "F2"},
    ]


def test_clean_issues_uncategorized(issue_data):
    grouped = markdown_issue.group_issues(issue_data)
    assert markdown_issue.clean_issues(grouped, "Uncategorized", ["description", "shortname", "boundary"]) == [
        {"description": "Nada 1", "shortname": "N1"},
        {"description": "Nada 2", "shortname": "N2"},
    ]


def test_add_facts(issue_data):
    grouped = markdown_issue.group_issues(issue_data)
    assert markdown_issue.add_facts(grouped) == (
        "### Facts\n\n"
        "  - description: Fact 1  \n"
        "    boundary: on  \n"
        "    shortname: F1 \n"
        "  - description: Fact 2  \n"
        "    shortname: F2 \n\n"
        )


def test_add_action_item():
    grouped = [
        {"category": "Action Item", "description": "Fact 1", "shortname": "F1", "boundary": "on", "keyUncertainty": "Unset", "decisionType": "Unset"},
        {"category": "Action Item", "description": "Fact 2", "shortname": "F2", "boundary": "Unset", "keyUncertainty": "Unset", "decisionType": "Unset"},
    ]
    assert markdown_issue.add_action_item(grouped) == (
        "### Action items\n\n"
        "  - description: Fact 1  \n"
        "    boundary: on  \n"
        "    shortname: F1 \n"
        "  - description: Fact 2  \n"
        "    shortname: F2 \n\n"
        )


def test_add_value_metric(issue_data):
    grouped = markdown_issue.group_issues(issue_data)
    assert markdown_issue.add_value_metric(grouped) == (
        "### Value metrics\n\n"
        "  - description: Value 1 <br>"
        "boundary: on <br>"
        "shortname: V1 <br> \n"
        "  - description: Value 2 <br>"
        "boundary: out <br>"
        "shortname: V2 <br> \n\n"
        )


def test_add_uncategorized(issue_data):
    grouped = markdown_issue.group_issues(issue_data)
    assert markdown_issue.add_uncategorized(grouped) == (
        "### Uncategorized\n\n"
        "  - description: Nada 1 <br>"
        "shortname: N1 <br> \n"
        "  - description: Nada 2 <br>"
        "shortname: N2 <br> \n\n"
        )


def test_add_decision(issue_data):
    grouped = markdown_issue.group_issues(issue_data)
    assert markdown_issue.add_decision(grouped) == (
        "### Decisions\n\n"
        "  - description: Decision 3 <br>"
        "boundary: in <br>"
        "shortname: D3 <br> \n"
        "  - description: Decision 4 <br>"
        "boundary: in <br>"
        "shortname: D4 <br> \n"
        "  - description: Decision 5 <br>"
        "boundary: in <br>"
        "shortname: D5 <br> \n"
        "  - description: Decision 1 <br>"
        "boundary: on <br>"
        "shortname: D1 <br> \n"
        "  - description: Decision 2 <br>"
        "boundary: out <br>"
        "shortname: D2 <br>"
        "decision type: Focus <br>"
        "alternatives: \n"
        "    - yes\n"
        "    - no\n\n"
        )



def test_add_uncertainty(issue_data):
    grouped = markdown_issue.group_issues(issue_data)
    assert markdown_issue.add_uncertainty(grouped) == (
        "### Uncertainties\n\n"
        "  - description: Uncertainty 2 <br>"
        "shortname: U2 <br>"
        "key decision: true <br>"
        "outcomes: \n"
        "     - blue \n"
        "     - red \n"
        "boundary: in <br> \n"
        "  - description: Uncertainty 3 <br>"
        "shortname: U3 <br>"
        )



# def test_group_issues_category(issue_data):
#     assert markdown_issue.group_issues_category(issue_data) == {
#         "Fact" : [
#             {"category": "Fact", "description": "Fact 1", "shortname": "F1", "boundary": "on"},
#             {"category": "Fact", "description": "Fact 2", "shortname": "F2"},
#         ],
#         "Decision" : [
#             {"category": "Decision", "description": "Decision 1", "shortname": "D1", "boundary": "on"},
#             {"category": "Decision", "description": "Decision 2", "shortname": "D2", "boundary": "out"},
#             {"category": "Decision", "description": "Decision 3", "shortname": "D3", "boundary": "in"},
#             {"category": "Decision", "description": "Decision 4", "shortname": "D4", "boundary": "in"},
#             {"category": "Decision", "description": "Decision 4", "shortname": "D4", "boundary": "in"},
#         ],
#         "Uncertainty" : [
#             {"category": "Uncertainty", "description": "Uncertainty 1", "shortname": "U1"},
#             {"category": "Uncertainty", "description": "Uncertainty 2", "shortname": "U2", "boundary": "in"}
#         ],
#         "Value Metric" : [
#             {"category": "Value Metric", "description": "Value 1", "shortname": "V1", "boundary": "on"},
#             {"category": "Value Metric", "description": "Value 2", "shortname": "V2", "boundary": "out"},
#         ],
#         "Action Item" : [],
#         "Uncategorized" : [
#             {"category": "", "description": "Nada 1", "shortname": "N1"},
#             {"category": "", "description": "Nada 2", "shortname": "N2"},
#         ],
#     }


# def test_group_issues_boundary(issue_data):
#     grouped_data = markdown_issue.group_issues_category(issue_data)
#     assert markdown_issue.group_issues_boundary(grouped_data) == {
#         "Fact" : {
#             "in": [],
#             "on": [
#                 {"category": "Fact", "description": "Fact 1", "shortname": "F1", "boundary": "on"},
#                 ],
#             "out": [],
#             "Unset": [
#                 {"category": "Fact", "description": "Fact 2", "shortname": "F2"},
#             ]
#         },
#         "Decision" : {
#             "in": [
#                 {"category": "Decision", "description": "Decision 3", "shortname": "D3", "boundary": "in"},
#                 {"category": "Decision", "description": "Decision 4", "shortname": "D4", "boundary": "in"},
#                 {"category": "Decision", "description": "Decision 5", "shortname": "D5", "boundary": "in"},
#             ],
#             "on": [
#                 {"category": "Decision", "description": "Decision 1", "shortname": "D1", "boundary": "on"},
#                 ],
#             "out": [
#                 {"category": "Decision", "description": "Decision 2", "shortname": "D2", "boundary": "out"},
#             ],
#             "Unset": []
#         },
#         "Uncertainty" : {
#             "in": [
#                 {"category": "Uncertainty", "description": "Uncertainty 2", "shortname": "U2", "boundary": "in"}
#             ],
#             "on": [],
#             "out": [],
#             "Unset": [
#                 {"category": "Uncertainty", "description": "Uncertainty 1", "shortname": "U1"},
#             ]
#         },
#         "Value Metric" : {
#             "in": [],
#             "on": [
#                 {"category": "Value Metric", "description": "Value 1", "shortname": "V1", "boundary": "on"},
#                 ],
#             "out": [
#                 {"category": "Value Metric", "description": "Value 2", "shortname": "V2", "boundary": "out"},
#                 ],
#             "Unset": []
#         },
#         "Action Item" : [],
#         "Uncategorized" : {
#             "in": [],
#             "on": [],
#             "out": [],
#             "Unset": [
#                 {"category": "", "description": "Nada 1", "shortname": "N1"},
#                 {"category": "", "description": "Nada 2", "shortname": "N2"},
#             ]
#         }
#     }
import ast
import json

import numpy as np

from ...models.issue import IssueCreate, IssueResponse, ProbabilityData


def _merge_probability_dtype(destination_dtype: str, source_dtype: str) -> str:
    """Merges the probability types of two issues

    Args:
        destination_dtype (str): type of the destination issue
        source_dtype (str): type of the dragged issue

    Returns:
        merged_dtype (str): merged probability type
    """
    if (
        destination_dtype == "DiscreteConditionalProbability"
        or source_dtype == "DiscreteConditionalProbability"
    ):
        merged_dtype = "DiscreteConditionalProbability"
    else:
        merged_dtype = "DiscreteUnconditionalProbability"
    return merged_dtype


def _merge_probability_variables(
    destination_variables: dict[str, list[str]],
    source_variables: dict[str, list[str]],
) -> dict[str, list[str]]:
    """
    Merge probability variables from the destination and source dictionaries.

    Args:
        destination_variables (Dict[str, List[str]]): The destination dictionary
                                                      containing probability
                                                      variables.
        source_variables (Dict[str, List[str]]): The source dictionary containing
                                                 probability variables.

    Returns:
        Dict[str, List[str]]: A dictionary containing merged probability variables
                              from both dictionaries.
    """
    # make sure first dimension has same name - valid for univariate cases only
    first_src_variable = list(source_variables)[0]
    first_dst_variable = list(destination_variables)[0]
    first_source_states = source_variables.pop(first_src_variable)
    source_variables[first_dst_variable] = first_source_states

    merged_variables = {}
    variables_key = list(destination_variables) + [
        item for item in source_variables if item not in destination_variables
    ]
    for key in variables_key:  # Union of keys from both dictionaries
        list1 = destination_variables.get(key, [])
        list2 = source_variables.get(key, [])
        # Preserve order and remove duplicates
        merged_list = list1 + [item for item in list2 if item not in list1]
        merged_variables[key] = merged_list
    return merged_variables


def _merge_probability_function(merged_variables: dict[str, list[str]]) -> np.ndarray:
    """
    Merge the variables in `merged_variables` and create a zero matrix with the
        correct dimensions.

    Args:
        merged_variables (Dict[str, List[str]]): A dictionary containing the
                                                 merged variables, where the
                                                 keys are the variable names
                                                 and the values are lists of
                                                 possible outcomes for each
                                                 variable.

    Returns:
        np.ndarray: A zero matrix with the dimensions based on the merged
                    variables.

    """
    outcomes_keys = list(merged_variables.keys())
    outcome_length = len(merged_variables[outcomes_keys[0]])
    other_arrays = [merged_variables[key] for key in outcomes_keys[1:]]
    condition_length = 1
    for arr in other_arrays:
        condition_length *= len(arr)

    # Create a zero matrix with the correct dimensions based on the
    # merged_variables dimensions
    merged_probability_function = np.zeros(
        (outcome_length, condition_length), dtype=float
    )
    return merged_probability_function


def _probability_merge(
    destination_probability: ProbabilityData,
    source_probability: ProbabilityData,
) -> ProbabilityData:
    """Merging ProbabilityData

        Defines the ProbabilityData.dtype based on the input, if one of them is
        a conditional probability, the new type will be a conditional
        probability as well.
        The variables are merged in a union operation, preserving the order of
        the dict and updates the lists in case of differences between possible
        outcomes and conditions.
        The merged probability_function is a zero matrix with the dimensions
        based on the merged variables.

    Args:
        source_probability (ProbabilityData): probability data of the dragged
                                              issue
        destination_probability (ProbabilityData): probability data of the
                                                   destination issue

    Returns:
        merged_probability (ProbabilityData): merged probability data

    """
    if not destination_probability and not source_probability:
        merged_probability = None
    elif not destination_probability:
        merged_probability = source_probability
    elif not source_probability:
        merged_probability = destination_probability
    else:
        merged_probability_dtype = _merge_probability_dtype(
            destination_probability.dtype, source_probability.dtype
        )

        merged_variables = _merge_probability_variables(
            destination_probability.variables, source_probability.variables
        )

        merged_probability_function = _merge_probability_function(merged_variables)

        merged_probability = ProbabilityData(
            dtype=merged_probability_dtype,
            variables=merged_variables,
            probability_function=merged_probability_function,
        )
    return merged_probability


def _merge_comments(dst, src):
    """Merge comment data

    Args:
        dst (CommentData): destination comment data
        src (CommentData): source comment data

    Returns:
        CommentData: Merged comments.
    """
    comments = []
    if dst.comments:
        comments += dst.comments
    if src.comments:
        comments += src.comments
    return comments


def _list_merge(str_list1, str_list2):
    """
    Merge two string lists and return the merged list as a string.

    Args:
        str_list1 (str): First string list.
        str_list2 (str): Second string list.

    Returns:
        str: Merged string list.
    """
    if not str_list1 and not str_list2:
        return ""
    elif not str_list1:
        return str_list2
    elif not str_list2:
        return str_list1
    else:
        list1 = ast.literal_eval(str_list1)
        list2 = ast.literal_eval(str_list2)
        merged_list = list1 + [item for item in list2 if item not in list1]
        merged_str_list = json.dumps(merged_list)
        return merged_str_list


def issue_merge(
    source_issue: IssueResponse, destination_issue: IssueResponse
) -> IssueCreate:
    """Merges the data of two issues

    Args:
        source_issue (IssueResponse): data of the dragged issue
        destination_issue (IssueResponse): data of the destination issue

    Returns:
        merged_data (IssueCreate): merged data for the two issues
    """

    merged_data = IssueCreate(
        category=destination_issue.category,
        index=destination_issue.index,
        shortname=destination_issue.shortname,
        tag=list(
            set(destination_issue.tag + source_issue.tag)
        ),  # Merge and remove duplicates
        description=destination_issue.description + " " + source_issue.description,
        keyUncertainty=(
            source_issue.keyUncertainty
            if destination_issue.keyUncertainty == source_issue.keyUncertainty
            else None
        ),
        decisionType=(
            source_issue.decisionType
            if source_issue.decisionType == destination_issue.decisionType
            else None
        ),
        alternatives=(destination_issue.alternatives or [])
        + [
            alternative
            for alternative in (source_issue.alternatives or [])
            if alternative not in (destination_issue.alternatives or [])
        ],  # list_merge(destination_issue.alternatives, source_issue.alternatives),
        probabilities=_probability_merge(
            destination_issue.probabilities, source_issue.probabilities
        ),
        influenceNodeUUID="",
        boundary=source_issue.boundary
        if (source_issue.boundary == destination_issue.boundary)
        else None,
        comments=_merge_comments(destination_issue, source_issue),
    )
    return merged_data

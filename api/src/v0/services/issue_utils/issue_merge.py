import ast
import json

from ...models.issue import (
    IssueCreate,
    IssueResponse,
    CommentData,
    UncertaintyData,
    DecisionData,
    ValueMetricData,
    DiscreteConditionalProbabilityData,
    DiscreteUnconditionalProbabilityData,
    none_probability_function,
    )


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
    

def _copy_if_same_or_none(dst, src):
    """return input if both input are equal, else None

    Args:
        dst (Any): a value
        src (Any): a value

    Returns:
        Any: dst if dst == src, else None
    """
    return dst if dst == src else None


def _concatenate_strings(dst: str, src: str) -> str:
    """Concatenate two strings with a space in between.

        If the 2 strings are identical, returns one of them.

    Args:
        dst (str): Fisrt string
        src (str): Second string

    Returns:
        str: Concatenated string
    """
    if dst == src:
        return dst
    return dst + " " + src


def _merge_probability_variables(
    dst_variables: dict[str, list[str]],
    src_variables: dict[str, list[str]],
) -> dict[str, list[str]]:
    """
    Merge probability variables from the dst and src dictionaries.

    Args:
        dst_variables (Dict[str, List[str]]): The dst dictionary
                                                      containing probability
                                                      variables.
        src_variables (Dict[str, List[str]]): The src dictionary containing
                                                 probability variables.
    Returns:
        Dict[str, List[str]]: A dictionary containing merged probability variables
                              from both dictionaries.
    """
    variables = list(dst_variables.keys()) + [
        item for item in list(src_variables.keys()) 
        if item not in list(dst_variables.keys())
        ]
    merged_variables = {}
    for key in variables:
        merged_variables[key] = list(dst_variables.get(key, [])) + \
            [item for item in src_variables.get(key, []) 
             if item not in dst_variables.get(key, [])]
    return merged_variables


def _merge_unconditional_probabilities(
    dst_probability: DiscreteUnconditionalProbabilityData,
    src_probability:  DiscreteUnconditionalProbabilityData,
) ->  DiscreteUnconditionalProbabilityData:
    """Merge 2 discrete unconditional probabilities

        Unique variables and states are kept.
        Merging 2 1D probabilities with different variable names leads to
        a 2D probabilities.
        Merging 2 1D probabilities with same variable name but different
        outcomes names leads to a 1D probability with a bigger number of possible
        outcomes.

    Args:
        dst_probability (DiscreteUnconditionalProbabilityData): First probability
        src_probability (DiscreteUnconditionalProbabilityData): Second probability

    Returns:
        DiscreteUnconditionalProbabilityData: Merged probability
    """
    merged_variables = _merge_probability_variables(
        dst_probability.variables, src_probability.variables
        )
    merged_probability_function = none_probability_function(merged_variables)
    return DiscreteUnconditionalProbabilityData(
            dtype = "DiscreteUnconditionalProbability",
            probability_function=merged_probability_function,
            variables=merged_variables,
        )


def _merge_conditional_and_unconditional_probabilities(
    conditional_probability: DiscreteConditionalProbabilityData,
    unconditional_probability:  DiscreteUnconditionalProbabilityData,
) ->  DiscreteConditionalProbabilityData:
    """Merge 2 discrete unconditional probabilities

        Unique variables and states are kept.
        Merging 2 1D probabilities with different variable names leads to
        a 2D probabilities.
        Merging 2 1D probabilities with same variable name but different
        outcomes names leads to a 1D probability with a bigger number of possible
        outcomes.

    Args:
        conditional_probability (DiscreteConditionalProbabilityData): 
        Conditional probability
        unconditional_probability  (DiscreteUnconditionalProbabilityData): 
        Unconditional probability

    Returns:
        DiscreteConditionalProbabilityData: Merged probability

    .. warning: 
        The merging will fail if some conditioning variable names are identical to
        some conditioned variable names.
        The merging will also fail if 2 parents have same variable names.
    """
    parents_uuid = conditional_probability.parents_uuid
    merged_conditioned_variables = _merge_probability_variables(
        conditional_probability.conditioned_variables,
        unconditional_probability.conditioned_variables
        )
    merged_conditioning_variables = conditional_probability.conditioning_variables
    merged_probability_function = none_probability_function(
        merged_conditioned_variables | merged_conditioning_variables
        )
    return DiscreteUnconditionalProbabilityData(
            dtype = "DiscreteConditionalProbability",
            probability_function=merged_probability_function,
            conditioned_variables=merged_conditioned_variables,
            conditioning_variables=merged_conditioning_variables,
            parents_uuid=parents_uuid
        )


def _merge_conditional_probabilities(
    dst_probability: DiscreteConditionalProbabilityData,
    src_probability:  DiscreteConditionalProbabilityData,
) ->  DiscreteConditionalProbabilityData:
    """Merge 2 discrete unconditional probabilities

        Unique variables and states are kept.
        Merging 2 1D probabilities with different variable names leads to
        a 2D probabilities.
        Merging 2 1D probabilities with same variable name but different
        outcomes names leads to a 1D probability with a bigger number of possible
        outcomes.

    Args:
        dst_probability (DiscreteConditionalProbabilityData): First probability
        src_probability  (DiscreteUnconditionalProbabilityData): Second probability

    Returns:
        DiscreteConditionalProbabilityData: Merged probability
    """
    # The merging of parents is done in the same way as the merging of variables.
    # These mergings should be kept consistent!
    parents_uuid = dst_probability.parents_uuid + [
        item for item in src_probability.parents_uuid 
        if item not in dst_probability.parents_uuid
        ]
    merged_conditioned_variables = _merge_probability_variables(
        dst_probability.conditioned_variables,
        src_probability.conditioned_variables
        )
    merged_conditioning_variables = _merge_probability_variables(
        dst_probability.conditioning_variables,
        src_probability.conditioning_variables
        )
    merged_probability_function = none_probability_function(
        merged_conditioned_variables | merged_conditioning_variables
        )
    return DiscreteUnconditionalProbabilityData(
            dtype = "DiscreteConditionalProbability",
            probability_function=merged_probability_function,
            conditioned_variables=merged_conditioned_variables,
            conditioning_variables=merged_conditioning_variables,
            parents_uuid=parents_uuid
        )


def _probability_merge(
    destination_probability: DiscreteUnconditionalProbabilityData | DiscreteConditionalProbabilityData | None,
    source_probability:  DiscreteUnconditionalProbabilityData | DiscreteConditionalProbabilityData | None,
) ->  DiscreteUnconditionalProbabilityData | DiscreteConditionalProbabilityData | None:
    """Merging Probabilities

        Defines the probability_type based on the input, if one of them is
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
    if not destination_probability:
        return source_probability
    if not source_probability:
        return destination_probability

    if destination_probability == source_probability:
        return destination_probability

    if (destination_probability.dtype == "DiscreteUnconditionalProbability" and
        source_probability.dtype == "DiscreteUnconditionalProbability"):
        return _merge_unconditional_probabilities(            
            destination_probability,
            source_probability
            )

    if (destination_probability.dtype == "DiscreteConditionalProbability" and
        source_probability.dtype == "DiscreteConditionalProbability"):
        return _merge_conditional_and_unconditional_probabilities(
            destination_probability,
            source_probability
        )
    if (destination_probability.dtype == "DiscreteConditionalProbability" and
        source_probability.dtype == "DiscreteUnconditionalProbability"):
        return _merge_conditional_and_unconditional_probabilities(
            source_probability,
            destination_probability
        )

    if (destination_probability.dtype == "DiscreteUnconditionalProbability" and
        source_probability.dtype == "DiscreteConditionalProbability"):
        return _merge_conditional_probabilities(
            destination_probability,
            source_probability
            )


def _merge_comments(
        dst: CommentData | None,
        src: CommentData | None
        ) -> list[str]  | None:
    """Merge comment data

    Args:
        dst (CommentData | None): destination comment data
        src (CommentData | None): source comment data

    Returns:
        CommentData | None: Merged comments.
    """
    comments = []
    if dst:
        comments += dst
    if src:
        comments += src
    return comments


def _merge_uncertainties(
        dst: UncertaintyData | None,
        src: UncertaintyData | None
        ) -> UncertaintyData | None:
    """Merge uncertainty data

    Args:
        dst (UncertaintyData | None): destination uncertainty data
        src (UncertaintyData | None): source uncertaity data

    Returns:
        UncertaintyData | None: Merged uncertainty.
    """
    if not src:
        return dst
    if not dst:
        return src
    probability=_probability_merge(dst.probability, src.probability)
    key = _copy_if_same_or_none(dst.key, src.key)
    source = _concatenate_strings(dst.source, src.source)
    return UncertaintyData(probability=probability, key=key, source=source)


def _merge_decisions(
    dst: DecisionData | None,
    src: DecisionData | None
    ) -> DecisionData | None:
    """Merge decision data

    Args:
        dst (DecisionData | None): destination decision data
        src (DecisionData | None): source uncertaity data

    Returns:
        DecisionData | None: Merged decision.
    """
    if not src:
        return dst
    if not dst:
        return src
    states = dst.states or [] + [
        alternative
        for alternative in (src.states or [])
        if alternative not in (dst.states or [])
    ]  # list_merge(dst.states, src.states),
    decision_type = _copy_if_same_or_none(dst.decision_type, src.decision_type)
    return DecisionData(states=states, decision_type=decision_type)


def _merge_value_metrics(
        dst: ValueMetricData | None,
        src: ValueMetricData | None
        ) -> ValueMetricData | None:
    """Merge value metric data

    Args:
        dst (ValueMetricData | None): destination value metric data
        src (ValueMetricData | None): source uncertaity data

    Returns:
        ValueMetricData | None: Merged value metric.
    """
    if not src:
        return dst
    if not dst:
        return src
    cost_function = _copy_if_same_or_none(dst.cost_function, src.cost_function)
    weigth = _copy_if_same_or_none(dst.weigth, src.weigth)
    return ValueMetricData(cost_function=cost_function, weigth=weigth)


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
        description=_concatenate_strings(
            destination_issue.description, source_issue.description
            ),
        uncertainty=_merge_uncertainties(
            destination_issue.uncertainty, source_issue.uncertainty
            ),
        decision=_merge_decisions(
            destination_issue.decision, source_issue.decision
            ),
        value_metric=_merge_value_metrics(
            destination_issue.value_metric, source_issue.value_metric
            ),
        boundary=_copy_if_same_or_none(
            destination_issue.boundary, source_issue.boundary
            ),
        comments=_merge_comments(destination_issue.comments, source_issue.comments),
    )
    return merged_data

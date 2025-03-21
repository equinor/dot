export const getDecisionRows = (decisionList) => {
  return decisionList.map((decision) => ({
    index: decision.index,
    description: decision.description,
    decisionType: decision.decisionType,
    tag: decision.tag,
    alternatives: decision.alternatives,
    shortname: decision.shortname,
    uuid: decision.uuid,
  }));
};

export const getUncertaintyRows = (uncertaintyList) => {
  return uncertaintyList.map((uncertainty) => {
    if (!uncertainty.probabilities) {
      return {
        index: uncertainty.index,
        description: uncertainty.description,
        keyUncertainty: uncertainty.keyUncertainty,
        tag: uncertainty.tag,
        outcomes: null,
        shortname: uncertainty.shortname,
        uuid: uncertainty.uuid,
      };
    }

    const firstVariableKey = Object.keys(
      uncertainty.probabilities.variables
    )[0];
    return {
      index: uncertainty.index,
      description: uncertainty.description,
      keyUncertainty: uncertainty.keyUncertainty,
      tag: uncertainty.tag,
      outcomes: uncertainty.probabilities.variables[firstVariableKey],
      shortname: uncertainty.shortname,
      uuid: uncertainty.uuid,
    };
  });
};

/**
 *
 *
 * @param {Object} modelJson
 * @returns {Object}
 */
export function chooseAnimalModelsSchema(animalModel) {
  return 'category' in animalModel ?
        useRevisedAnimalModelsSchema(animalModel) : usePreviousAnimalModelsSchema(animalModel);
}

/**
 *
 *
 * @param {Object} modelJson
 * @returns {Object}
 */
export function useRevisedAnimalModelsSchema(modelJson) {
  const strucutreNewConditionRelations = (conditionRelationsList) => {
    return conditionRelationsList.filter((condition) => {
      return condition.conditionRelationType?.name == 'has_condition';
    }).reduce((hasConditions, conditionRelation) => {
      const conditionSummaries = conditionRelation.conditions.map((summary) => {
        return {conditionStatement: summary.conditionSummary};
      });
      hasConditions.push(...conditionSummaries);
      return hasConditions;
    }, []);
  };

  return {
    ...(modelJson.model?.agmFullName?.['displayText']) && {'name': modelJson.model.agmFullName.displayText},
    ...(modelJson.model?.agmFullName?.['displayText']) && {'background': modelJson.model.agmFullName.displayText},
    ...(modelJson.model?.dataProvider?.['abbreviation']) && {'source': modelJson.model.dataProvider.abbreviation},
    ...(modelJson.hasPhenotypeAnnotations) && {'phenotypes': modelJson.associatedPhenotype},
    ...(modelJson.hasDiseaseAnnotations) && {'diseaseModels': modelJson.diseaseModels},
    ...('conditionRelations' in modelJson) &&
      {'conditions': strucutreNewConditionRelations(modelJson['conditionRelations'])},
  };
};

/**
 *
 *
 * @param {Object} modelJson
 * @returns {Object}
 */
export function usePreviousAnimalModelsSchema(modelJson) {
  return {
    ...('name' in modelJson) && {'name': modelJson.name},
    ...('name' in modelJson) && {'background': modelJson.name},
    ...('source' in modelJson) && {'source': modelJson.source.name},
    ...('phenotypes' in modelJson) && {'phenotypes': modelJson.phenotypes},
    ...('diseaseModels' in modelJson) && {'diseaseModels': modelJson.diseaseModels},
    ...(modelJson?.conditions?.has_condition) && {'conditions': modelJson.conditions.has_condition},
  };
};

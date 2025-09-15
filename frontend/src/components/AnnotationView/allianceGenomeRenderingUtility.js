/**
 * Chooses the method to adapt the different animal model JSON schemas.
 *
 * @param {Object} animalModel - The animal model data object to transform.
 * @returns {Object} - A structured object with selected and formatted fields.
 */
export function chooseAnimalModelsSchema(animalModel) {
  return 'category' in animalModel ?
        useRevisedAnimalModelsSchema(animalModel) : usePreviousAnimalModelsSchema(animalModel);
}


/**
 * Transforms an animal model JSON using the revised schema format.
 *
 * @param {Object} modelJson - The raw animal model data object.
 * @returns {Object} - A structured object with selected and formatted fields.
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

  const dataProviderModelUrl = {
    'ZFIN': 'https://zfin.org/',
    'MGI': 'https://www.informatics.jax.org/allele/genoview/',
    'RGD': 'https://rgd.mcw.edu/rgdweb/report/strain/main.html?id=',
  };

  const dataProvider = modelJson.model?.dataProvider?.['abbreviation'];

  return {
    ...(modelJson.model?.agmFullName?.['displayText']) && {'name': modelJson.model.agmFullName.displayText},
    ...(dataProvider && modelJson.model?.primaryExternalId && dataProvider in dataProviderModelUrl) &&
      {'modelUrl': dataProviderModelUrl[dataProvider] + modelJson.model.primaryExternalId},
    ...(modelJson.model?.agmFullName?.['displayText']) && {'background': modelJson.model.agmFullName.displayText},
    ...(modelJson.model?.dataProvider?.['abbreviation']) && {'source': modelJson.model.dataProvider.abbreviation},
    ...(modelJson.hasPhenotypeAnnotations) && {'phenotypes': modelJson.associatedPhenotype},
    ...(modelJson.hasDiseaseAnnotations) && {'diseaseModels': modelJson.diseaseModels},
    ...('conditionRelations' in modelJson) &&
      {'conditions': strucutreNewConditionRelations(modelJson['conditionRelations'])},
  };
};


/**
 * Transforms an animal model object using the legacy schema format.
 *
 * @param {Object} modelJson - The raw animal model data object.
 * @returns {Object} - A structured object with selected and formatted fields.
 */
export function usePreviousAnimalModelsSchema(modelJson) {
  return {
    ...('name' in modelJson) && {'name': modelJson.name},
    ...('url' in modelJson) && {'modelUrl': modelJson.url},
    ...('name' in modelJson) && {'background': modelJson.name},
    ...('source' in modelJson) && {'source': modelJson.source.name},
    ...('phenotypes' in modelJson) && {'phenotypes': modelJson.phenotypes},
    ...('diseaseModels' in modelJson) && {'diseaseModels': modelJson.diseaseModels},
    ...(modelJson?.conditions?.has_condition) && {'conditions': modelJson.conditions.has_condition},
  };
};

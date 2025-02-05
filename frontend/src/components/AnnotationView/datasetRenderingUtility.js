export function isDatasetAvailable(datasetValue) {
  return datasetValue == '.' || datasetValue == 'null' || datasetValue == null;
}
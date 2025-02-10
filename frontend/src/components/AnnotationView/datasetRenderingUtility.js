export function isDatasetAvailable(datasetValue) {
  return !(
    datasetValue == undefined ||
    datasetValue == '.' ||
    datasetValue == 'null' ||
    datasetValue == null ||
    datasetValue == ""
  );
}

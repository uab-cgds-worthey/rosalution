"""General test utilities for the application"""
import json
import os

from unittest.mock import AsyncMock, MagicMock

DATABSE_FIXTURE_PATH = "../../etc/fixtures/initial-seed/"
UNIT_TEST_FIXTURE_PATH = "./fixtures/"
ASSETS_FIXTURE_PATH = f"{UNIT_TEST_FIXTURE_PATH}assets/"


def rosalution_filepath():
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    return os.path.join(current_directory, '../../')


def fixture_path():
    """Returns the fixture data binary"""
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    return os.path.join(current_directory, UNIT_TEST_FIXTURE_PATH)


def integration_database_fixture_filepath():
    """Returns the fixture data binary"""
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    return os.path.join(current_directory, UNIT_TEST_FIXTURE_PATH + "integration-mongodb-database/")


def assets_fixture_filepath(filename):
    """Returns the fixture data binary"""
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    return os.path.join(current_directory, ASSETS_FIXTURE_PATH + filename)


def fixture_filepath(filename):
    """Returns the fixture data binary"""
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    return os.path.join(current_directory, ASSETS_FIXTURE_PATH + filename)


def read_assset_fixture(fixture_name):
    return read_fixtures(ASSETS_FIXTURE_PATH, fixture_name)


def read_database_fixture(fixture_filename):
    """reads the JSON from the filepath relative to the database fixtures in etc"""
    return read_fixtures(DATABSE_FIXTURE_PATH, fixture_filename)


def read_test_fixture(fixture_filename):
    """reads the JSON from the filepath relative to the tests"""
    return read_fixtures(UNIT_TEST_FIXTURE_PATH, fixture_filename)


def read_fixtures(base_path, fixture_filename):
    """With a base path relative to the current directory, loads a fixture for fixture_filename"""
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    path_to_file = os.path.join(current_directory, base_path + fixture_filename)
    with open(path_to_file, mode="r", encoding="utf-8") as file_to_open:
        data = json.load(file_to_open)
        file_to_open.close()

    return data


def mock_mongo_collection():
    """
    Returns the annotation collection for the configuration to verify
    annotation tasks are created according to the configuration
    """
    fake_mongodb_cursor = AsyncMock()
    fake_mongodb_cursor.to_list.return_value = []
    mock_collection = AsyncMock()
    mock_collection.aggregate = AsyncMock()
    mock_collection.find = AsyncMock(return_value=fake_mongodb_cursor)
    mock_collection.find_one = AsyncMock()
    mock_collection.update_one = AsyncMock()
    mock_collection.insert_one = AsyncMock()
    mock_collection.find_one_and_update = AsyncMock()
    mock_collection.count_documents = AsyncMock()
    return mock_collection


def magic_mock_mongo_collection():
    """
    Returns the annotation collection for the configuration to verify
    annotation tasks are created according to the configuration
    """
    mock_collection = MagicMock()
    mock_collection.aggregate = MagicMock()
    mock_collection.find = MagicMock()
    mock_collection.find_one = MagicMock()
    mock_collection.update_one = MagicMock()
    mock_collection.insert_one = MagicMock()
    mock_collection.find_one_and_update = MagicMock()
    mock_collection.count_documents = MagicMock()
    return mock_collection


def mock_gridfs_bucket():
    """Returns a mocked GridFS bucket"""
    mock_bucket = AsyncMock()
    mock_bucket.open_download_stream = AsyncMock()
    mock_bucket.open_upload_stream = AsyncMock()
    mock_bucket.put = AsyncMock()
    mock_bucket.get = AsyncMock()
    mock_bucket.list = AsyncMock()
    mock_bucket.exists = AsyncMock()
    mock_bucket.delete = AsyncMock()
    return mock_bucket


def magic_mock_gridfs_bucket():
    """Returns a mocked GridFS bucket"""
    mock_bucket = MagicMock()
    mock_bucket.open_download_stream = MagicMock()
    mock_bucket.open_upload_stream = MagicMock()
    mock_bucket.put = MagicMock()
    mock_bucket.get = MagicMock()
    mock_bucket.list = MagicMock()
    mock_bucket.exists = MagicMock()
    mock_bucket.delete = MagicMock()
    return mock_bucket


# Disabling PyLint due to this being a simple Mock adapter as a simple test harness for emulating mising a dependency
class SkipDependencies:  # pylint: disable=too-few-public-methods
    """ A skip annotation dependencies helper class that allows tester to dictate which datasets to skip once to
    emulate a depedency not existing the first time when preparing an Annotation Task for annotation."""

    def __init__(self, dependencies_to_skip=["HGNC_ID"]):
        """ Dictating the list of  of dataset names to emulate that dataset annotation not existing."""
        self.skip_tracker = {}
        self.to_skip = dependencies_to_skip

    async def skip_find_genomic_unit_annotation_value_mock(self, *args):
        """ Mock method that tracks if the provided dependencies are one of the ones indicated to skip"""
        annotation_unit = args[0]
        name = annotation_unit.get_dataset_name()
        genomic_unit = annotation_unit.get_genomic_unit()
        should_skip = (name in self.to_skip and name not in self.skip_tracker)
        return self.skip_tracker.setdefault(name, None) if should_skip else f"{genomic_unit}-{name}-value"


class SkipManifestEntriesExist:  # pylint: disable=too-few-public-methods
    """ A skip annotation dependencies helper class that allows tester to dictate which datasets to skip once to
    emulate a depedency not existing the first time when preparing an Annotation Task for annotation."""

    def __init__(self, dependencies_to_exist=["HPO_NCBI_GENE_ID"], dependencies_to_skip=["HGNC_ID"]):
        """ Dictating the list of  of dataset names to emulate that dataset annotation not existing."""
        self.skip_tracker = {}
        self.mock_manifest_entry = {}
        self.dependencies_to_exist = dependencies_to_exist
        self.dependencies_to_skip = dependencies_to_skip

        for dataset in (*dependencies_to_skip, *dependencies_to_exist):
            self.skip_tracker[dataset] = 0
            self.mock_manifest_entry[dataset] = {
                "data_set": "mock-dataset", "data_source": "mock-datasource", "version": "fake-version"
            }

    def set_analysis_manifest_entry(self, dataset_name: str, dependency_manifest_entry: dict):
        self.mock_manifest_entry[dataset_name] = dependency_manifest_entry

    async def fake_get_manifest_dataset_config(self, *args):
        """ Mock method that tracks if the provided dependencies are one of the ones indicated to skip"""
        analysis_name, genomic_unit, dataset_name = args

        #the dependency will not get its manifest entry checked and need to exist to annotate
        if dataset_name not in self.skip_tracker:
            print("no manifest entry, not tracked dependency", dataset_name)
            return None

        expected_skip_count_completed = 2 if dataset_name in self.dependencies_to_exist else 2
        self.skip_tracker[dataset_name] += 1
        print("tracked dependency increamented from call: ", dataset_name, self.skip_tracker[dataset_name])
        if expected_skip_count_completed < self.skip_tracker[dataset_name]:
            print("returning manifest entry: ", not self.skip_tracker[dataset_name] > expected_skip_count_completed)
            return self.mock_manifest_entry[dataset_name]

        print("returning none for fake manifest entry for dependency")

        return None


# class AnnotateTracker:
#     def __init__(self, initial_queue):
#         self.annotation_tracker = {}

#         for unit in initial_queue.queue:
#             self.annotation_tracker[unit] = {
#                 'analysis_manifest_entry_exist': False,
#                 'task_annotate_called': True
#             }

# For CPAM 46, LMNA HGNC_ID, depedency for CLingGen annotation
# 1. HGNCID hasn't been annotated yet
#.  process_annotation_unit()
#       1. check if analysis has a manfiest entry for LMNA HGNCID, It should not
#       2. does the annotation unit have a clauclated version, NO
#       2.a handle getting teh version
#       2.b Creating a Version Task to calculate the version, (pushed onto the same thread loop)
#       3. EXIT process_annotation unit
#.  process annotation unit - CLinGen for LMNA
#       1. check if analysis has manifest entry for Clingen LMNA, NOne
#       2. does the annotation unit have a clauclated version, NO
#       2.a handle getting teh version
#       2.b Creating a Version Task to calculate the version, (pushed onto the same thread loop)
#       3. EXIT process_annotation unit
#.  version task for LMNA HNCDID complete, update annotation unit, push back onto original queue
#.  process_annotation_unit()
#        1. check if analysis has manifest entry, NOPE
#       2. version HAS been calculated
#       # no dependencies, create annotation task, put onto event loop
#.  version task for LMNA ClinGen complete, update annotation unit, push back onto original queue
#.  process_annotation_unit()
#       1. no manifest entry, but has calcualted verison
#       2. has calcualte version
#       3. HAS DEPENENCIES
#       4. for each depedency (HGNCID)
#       4.a #get all of the missing ones (hgnc_id is not an attribute on annotation unit)
#       4b. for each missing depepdency
#            Get Manifest Entry for HGNCID, does the entry eist
#           NO Entry Exists, meaning can't get depepency,
#       finsih depency gather
#       process-annotation-unit, checks if annotation unit ClingGen is READY to annotate,
#           # no it isn't, because its missing depepdencies (HGNC_ID)
#           #put back onto the incoming annotation queue
#
#.  handle_on_annotation_task_complete thread, annotate task for LMNA HNCDID completed
#       adds manifest entry to mongodb for analysis
#       extract and save value to database
#   Clingen LMNA process
#.  process_annotation_unit()
#       1. no manifest entry, but has calcualted verison
#       2. has calcualte version
#       3. HAS DEPENENCIES
#       4. for each depedency (HGNCID)
#       4.a #get all of the missing ones (hgnc_id is not an attribute on annotation unit)
#       4b. for each missing depepdency
#            Get Manifest Entry for HGNCID, does the entry eist
#            YES, manifest entry exists
#           Get the value from genomic unit collection, using the manifest entry information gathered
#       5. finsih depency gather
#       6. process-annotation-unit, checks if unit clingen is ready
#       6.a IT IS READY, all conditions met, create task to annotate Clingen LMNA
#

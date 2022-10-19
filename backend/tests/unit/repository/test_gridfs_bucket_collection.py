"""Tests gridfs bucket collection"""


def test_filename_exists(gridfs_bucket_collection):
    """Tests the filename_exists function"""
    actual = gridfs_bucket_collection.filename_exists("test.txt")
    assert actual is True


def test_save_file(gridfs_bucket_collection):
    """Tests the save_file function"""
    actual = gridfs_bucket_collection.save_file(
        "This is a test file", "test.txt")
    assert actual == "633afb87fb250a6ea1569555"


def test_if_id_exists(gridfs_bucket_collection):
    """Tests the check_if_id_exists function"""
    actual = gridfs_bucket_collection.check_if_id_exists(
        "633afb87fb250a6ea1569555")
    assert actual is True


def test_list_files(gridfs_bucket_collection):
    """Tests the list_files function"""
    actual = gridfs_bucket_collection.list_files()
    assert len(actual) == 1
    assert actual[0] == "test.txt"


def test_find_file_by_name(gridfs_bucket_collection):
    """Tests the find_file_by_name function"""
    actual = gridfs_bucket_collection.find_file_by_name("test.txt")
    assert actual == b"This is a test file"


def test_delete_file(gridfs_bucket_collection):
    """Tests the delete function"""
    actual = gridfs_bucket_collection.delete("633afb87fb250a6ea1569555")
    assert actual is None

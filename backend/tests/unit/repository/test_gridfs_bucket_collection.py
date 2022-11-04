"""Tests gridfs bucket collection"""


def test_filename_exists(gridfs_bucket_collection):
    """Tests the filename_exists function"""
    actual = gridfs_bucket_collection.filename_exists("test.txt")
    assert actual is True


def test_save_file(gridfs_bucket_collection):
    """Tests the save_file function"""
    actual = gridfs_bucket_collection.save_file("This is a test file", "test.txt")
    assert actual == "633afb87fb250a6ea1569555"


def test_if_id_exists(gridfs_bucket_collection):
    """Tests the check_if_id_exists function"""
    actual = gridfs_bucket_collection.id_exists("633afb87fb250a6ea1569555")
    assert actual is True


def test_if_id_does_not_exist(gridfs_bucket_collection):
    """Tests the check_if_id_exists function"""
    actual = gridfs_bucket_collection.id_exists("63-3afb87-fb250a6ea156-9555")
    assert actual is False


def test_get_file(gridfs_bucket_collection):
    """Tests the get_file function"""
    actual = gridfs_bucket_collection.get_file("633afb87fb250a6ea1569555")
    assert actual == "test.txt"


def test_list_files(gridfs_bucket_collection):
    """Tests the list_files function"""
    actual = gridfs_bucket_collection.list_files()
    assert len(actual) == 1
    assert actual[0] == "test.txt"


def test_delete_file(gridfs_bucket_collection):
    """Tests the delete function"""
    actual = gridfs_bucket_collection.delete_file("633afb87fb250a6ea1569555")
    assert actual is None

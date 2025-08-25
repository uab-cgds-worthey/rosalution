"""Tests to verify Analysis operations"""
import pytest

from src.enums import GenomicUnitType


def test_get_units_to_annotate(units_to_annotate):
    """tests the number of units to annotate"""
    assert len(units_to_annotate) == 3


def test_get_genes_in_units_to_annotate(units_to_annotate):
    """Tests the list of genes returned"""
    genes = list(filter(lambda x: GenomicUnitType.GENE == x["type"], units_to_annotate))
    gene_names = list(map(lambda x: x["unit"], genes))
    assert len(gene_names) == 1
    assert "VMA21" in gene_names


def test_get_variants_in_units_to_annotate(units_to_annotate):
    """Tests the list of variants returned"""
    variants = list(filter(lambda x: GenomicUnitType.HGVS_VARIANT == x["type"], units_to_annotate))
    variant_names = list(map(lambda x: x["unit"], variants))
    assert len(variant_names) == 1
    assert "NM_001017980.3:c.164G>T" in variant_names


def test_get_transcripts_in_units_to_annotate(units_to_annotate):
    """Tests the list of transcripts returned"""
    transcripts = list(filter(lambda x: GenomicUnitType.TRANSCRIPT == x["type"], units_to_annotate))
    transcript_names = list(map(lambda x: x["unit"], transcripts))
    assert len(transcript_names) == 1
    assert "NM_001017980.3" in transcript_names


def test_finding_section_field_by_attachment_id(cpam0002_analysis):
    """Tests finding the section and field that has the following attachment"""
    section, field = cpam0002_analysis.find_section_field_by_attachment_id("601d43243c1-c326-48ba-9f69-8fb3fds17")
    assert section.header == "Mus musculus (Mouse) Model System"
    assert field['field'] == "Veterinary Pathology Imaging"
    assert field['value'][0]['name'] == "The Art of Inuyasha"


def test_fail_finding_section_field_by_attachment_id(cpam0002_analysis):
    """Tests finding the section and field that has the following attachment"""
    section, field = cpam0002_analysis.find_section_field_by_attachment_id("60234243c1-c326-48ba-9f69-8fb3fds17")
    assert section is None
    assert field is None


def test_find_dicussion_post(cpam0002_analysis):
    """ Finds a discussion post matching the post_id """
    found_post = cpam0002_analysis.find_discussion_post("9027ec8d-6298-4afb-add5-6ef710eb5e98")

    assert found_post['author_id'] == 'johndoe-client-id'
    assert found_post['author_fullname'] == 'Developer Person'


def test_find_dicussion_post_not_found(cpam0002_analysis):
    """ Finds a discussion post matching the post_id """
    found_post = cpam0002_analysis.find_discussion_post("fake-post-id-failure")

    assert found_post is None


def test_find_authored_discussion_post(cpam0002_analysis):
    """ Tests that a discussion post is returned matching a post id and client id """
    discussion_post_id = "e6023fa7-b598-416a-9f42-862c826255ef"
    client_id = 'johndoe-client-id'

    found_post = cpam0002_analysis.find_authored_discussion_post(discussion_post_id, client_id)

    assert found_post['author_id'] == client_id
    assert found_post['author_fullname'] == 'Variant Review Report Preparer Person'


def test_find_authored_discussion_post_failure_missing_post(cpam0002_analysis):
    """ Tests that a ValueError is thrown if no discussion post is found matching the post_id """
    discussion_post_id = "fake-post-id-failure"
    client_id = 'exqkhvidr7uh2ndslsdymbzfbmqjlunk'

    try:
        cpam0002_analysis.find_authored_discussion_post(discussion_post_id, client_id)
    except ValueError as error:
        assert isinstance(error, ValueError)
        assert str(error) == f"Post '{discussion_post_id}' does not exist."


def test_find_authored_discussion_post_author_mismatch(cpam0002_analysis):
    """ Test that no post is returned if a post is found, but the author's client id does not match """
    discussion_post_id = "e6023fa7-b598-416a-9f42-862c826255ef"
    client_id = 'fake-client-id-failure'

    found_post = cpam0002_analysis.find_authored_discussion_post(discussion_post_id, client_id)

    assert found_post is None


def test_attachment_exists_in_analysis(cpam0002_analysis):
    """ Test that no post is returned if a post is found, but the author's client id does not match """

    actual_file_attached = cpam0002_analysis.is_file_attached("633afb87fb250a6ea1569555")

    assert actual_file_attached is True


def test_attachment_doesnt_exist_in_analysis(cpam0002_analysis):
    """ Test that no post is returned if a post is found, but the author's client id does not match """

    actual_file_attached = cpam0002_analysis.is_file_attached("68a761c9bd16bc0a0c98062e")

    assert actual_file_attached is False


@pytest.fixture(name="units_to_annotate")
def fixture_units_to_annotate(cpam0002_analysis):
    """Fixture for the units to annotate for the CPAM0002 Analysis"""
    return cpam0002_analysis.units_to_annotate()

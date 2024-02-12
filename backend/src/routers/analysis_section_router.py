"""Analysis endpoints that for adding/updating/removing images, documents, links, and text fields of an analysis."""

import logging

from typing import List
from fastapi import APIRouter, Depends, File, Form, HTTPException, Response, Security, status, UploadFile

from ..dependencies import database
from ..enums import SectionRowType
from ..models.analysis import Analysis, Section
from ..security.security import get_authorization

router = APIRouter(tags=["analysis sections"], dependencies=[Depends(database)])

logger = logging.getLogger(__name__)


def add_file_to_bucket_repository(file_to_save, bucket_repository):
    """Saves the 'file_to_save' within the bucket repository and returns the files new uuid."""
    return bucket_repository.save_file(file_to_save.file, file_to_save.filename, file_to_save.content_type)


@router.post("/{analysis_name}/sections/batch", response_model=List[Section])
def update_many_analysis_sections(
    analysis_name: str,
    updated_sections: List[Section],
    repositories=Depends(database),
    authorized=Security(get_authorization, scopes=["write"])  #pylint: disable=unused-argument
):
    """Updates the sections that have changes"""

    repositories["analysis"].update_analysis_sections(analysis_name, updated_sections)
    updated_analysis = repositories["analysis"].find_by_name(analysis_name)
    updated_analysis_model = Analysis(**updated_analysis)
    return updated_analysis_model.sections


@router.post("/{analysis_name}/sections", response_model=List[Section])
def update_analysis_section(
    response: Response,
    analysis_name: str,
    row_type: SectionRowType,
    updated_section: Section = Form(...),
    upload_file: UploadFile = File(None),
    repositories=Depends(database),
    # authorized=Security(get_authorization, scopes=["write"])  #pylint: disable=unused-argument
):
    """Updates a section with the changed fields"""
    if row_type not in (SectionRowType.TEXT, SectionRowType.IMAGE, SectionRowType.DOCUMENT, SectionRowType.LINK):
        raise HTTPException(status_code=422, detail=f"'Unsupported 'row_type': {row_type}.")

    if row_type == SectionRowType.TEXT:
        for field in updated_section.content:
            field_name, field_value = field["fieldName"], field["value"]
            if "Nominator" == field_name:
                repositories["analysis"].update_analysis_nominator(analysis_name, '; '.join(field_value))
            repositories["analysis"].update_analysis_section(
                analysis_name, updated_section.header, field_name, {"value": field_value}
            )

    updated_field = updated_section.content[0]

    if row_type in (SectionRowType.IMAGE, SectionRowType.DOCUMENT):
        try:
            new_file_object_id = add_file_to_bucket_repository(upload_file, repositories["bucket"])
        except Exception as exception:
            raise HTTPException(status_code=500, detail=str(exception)) from exception

        if row_type == SectionRowType.DOCUMENT:
            field_value_file = {
                "name": upload_file.filename, "attachment_id": str(new_file_object_id), "type": "file", "comments": ""
            }
            repositories["analysis"].attach_section_supporting_evidence_file(
                analysis_name, updated_section.header, updated_field["fieldName"], field_value_file
            )

        if row_type == SectionRowType.IMAGE:
            repositories["analysis"].add_section_image(
                analysis_name, updated_section.header, updated_field["fieldName"], new_file_object_id
            )

    if row_type in (SectionRowType.LINK):
        field_value_link = {
            "name": updated_field["linkName"], "data": updated_field["link"], "type": "link", "comments": ""
        }

        repositories["analysis"].attach_section_supporting_evidence_link(
            analysis_name, updated_section.header, updated_field["fieldName"], field_value_link
        )

    response.status_code = status.HTTP_201_CREATED
    updated_analysis_model = Analysis(**repositories["analysis"].find_by_name(analysis_name))
    return updated_analysis_model.sections


@router.delete(
    "/{analysis_name}/sections/{attachment_id}", response_model=List[Section], status_code=status.HTTP_200_OK
)
def remove_section_attachment_from_field(
    analysis_name: str,
    attachment_id: str,
    repositories=Depends(database),
    authorized=Security(get_authorization, scopes=["write"])  #pylint: disable=unused-argument
):
    """ Removes a supporting evidence file from an analysis section """
    found_analysis = repositories['analysis'].find_by_name(analysis_name)

    if not found_analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unable to remove attachment with id '{attachment_id}'. Analysis '{analysis_name}' does not exist.'"
        )

    analysis = Analysis(**found_analysis)

    section, field = analysis.find_section_field_by_attachment_id(attachment_id)

    if not section or not field:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No section or field contains '{attachment_id}' attachment.'"
        )

    if repositories["bucket"].id_exists(attachment_id):
        repositories["bucket"].delete_file(attachment_id)

    return repositories['analysis'].remove_section_attachment(
        analysis_name, section.header, field['field'], attachment_id
    )


@router.put("/{analysis_name}/sections/{attachment_id}", response_model=List[Section])
def update_analysis_section_image( # pylint: disable=too-many-arguments
    analysis_name: str,
    attachment_id: str,
    row_type: SectionRowType,
    updated_section: Section = Form(...),
    upload_file: UploadFile = File(None),
    repositories=Depends(database),
    authorized=Security(get_authorization, scopes=["write"])  #pylint: disable=unused-argument
):
    """
    Replaces the existing image by the file identifier with the uploaded one or updates a section with changed field.
    """
    # This needs try catch like in annotation router - what was this old comment

    if row_type not in (SectionRowType.TEXT, SectionRowType.IMAGE):
        raise HTTPException(status_code=422, detail=f"'Unsupported 'row_type': {row_type}.")

    section_name = updated_section.header
    updated_field = updated_section.content[0]
    field_name = updated_field['fieldName']

    updated_analysis_sections = None

    if row_type is SectionRowType.IMAGE:
        new_file_id = repositories["bucket"].save_file(upload_file.file, upload_file.filename, upload_file.content_type)
        updated_analysis_sections = repositories['analysis'].update_section_image(
            analysis_name, section_name, field_name, new_file_id, attachment_id
        )
    elif row_type is SectionRowType.TEXT:
        new_field_value = updated_field['value']
        if "Nominator" == field_name:
            repositories["analysis"].update_analysis_nominator(analysis_name, '; '.join(new_field_value))
        repositories["analysis"].update_analysis_section(
            analysis_name, updated_section.header, field_name, {"value": new_field_value}
        )
        updated_analysis = repositories["analysis"].find_by_name(analysis_name)
        updated_analysis_model = Analysis(**updated_analysis)
        updated_analysis_sections = updated_analysis_model.sections

    if updated_analysis_sections is None:
        raise HTTPException(status_code=404, detail="Operation failed; contact system administrator.")

    return updated_analysis_sections

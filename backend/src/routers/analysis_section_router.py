# pylint: disable=too-many-arguments
"""Analysis endpoints that for adding/updating/removing images, documents, links, and text fields of an analysis."""

from typing import List
from fastapi import APIRouter, Depends, File, Form, HTTPException, Response, Security, status, UploadFile

from ..dependencies import database
from ..enums import SectionRowType
from ..models.analysis import Analysis, Section
from ..security.security import get_authorization

router = APIRouter(tags=["analysis sections"], dependencies=[Depends(database)])


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


@router.put("/{analysis_name}/section/remove/file")
def remove_animal_model_system_report(
    analysis_name: str,
    section_name: str = Form(...),
    field_name: str = Form(...),
    attachment_id: str = Form(...),
    repositories=Depends(database),
    authorized=Security(get_authorization, scopes=["write"])  #pylint: disable=unused-argument
):
    """ Removes a supporting evidence file from an analysis section """

    if repositories["bucket"].id_exists(attachment_id):
        repositories["bucket"].delete_file(attachment_id)

    return repositories['analysis'].remove_section_supporting_evidence(analysis_name, section_name, field_name)


@router.put("/{analysis_name}/section/remove/link")
def remove_animal_model_system_imaging(
    analysis_name: str,
    section_name: str = Form(...),
    field_name: str = Form(...),
    repositories=Depends(database),
    authorized=Security(get_authorization, scopes=["write"])  #pylint: disable=unused-argument
):
    """ Removes a supporting evidence link from an analysis section """

    return repositories["analysis"].remove_section_supporting_evidence(analysis_name, section_name, field_name)


@router.put("/{analysis_name}/section/update/{old_file_id}")
def update_analysis_section_image(
    analysis_name: str,
    old_file_id: str,
    upload_file: UploadFile = File(...),
    section_name: str = Form(...),
    field_name: str = Form(...),
    repositories=Depends(database),
    authorized=Security(get_authorization, scopes=["write"])  #pylint: disable=unused-argument
):
    """ Replaces the existing image by the file identifier with the uploaded one. """
    # This needs try catch like in annotation router
    new_file_id = repositories["bucket"].save_file(upload_file.file, upload_file.filename, upload_file.content_type)

    repositories['analysis'].update_section_image(analysis_name, section_name, field_name, new_file_id, old_file_id)

    return {'section': section_name, 'field': field_name, 'image_id': str(new_file_id)}


@router.delete("/{analysis_name}/section/remove/{file_id}")
def remove_analysis_section_image(
    analysis_name: str,
    file_id: str,
    section_name: str = Form(...),
    field_name: str = Form(...),
    repositories=Depends(database),
    authorized=Security(get_authorization, scopes=["write"])  #pylint: disable=unused-argument
):
    """ Removes the image from an analysis section's field by its file_id """
    try:
        repositories['analysis'].remove_analysis_section_file(analysis_name, section_name, field_name, file_id)
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception

    try:
        return repositories["bucket"].delete_file(file_id)
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception

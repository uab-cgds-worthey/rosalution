""" Analysis endpoint routes that serve up information regarding anaysis cases for rosalution """
import json

from typing import List, Union

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import StreamingResponse

from ..core.annotation import AnnotationService
from ..core.phenotips_importer import PhenotipsImporter
from ..dependencies import database, annotation_queue
from ..models.analysis import Analysis, AnalysisSummary
from ..models.phenotips_json import BasePhenotips

# This is temporarily changed as security is removed for the analysis endpoints to make development easier
# Change line 18 to the following to enable security:
# dependencies=[Depends(database), Security(get_authorization, scopes=["write"])]
# and add the following dependencies at the top:
# from fastapi import Security
# from ..security.security import get_authorization
router = APIRouter(prefix="/analysis",
                   tags=["analysis"], dependencies=[Depends(database)])


@router.get("/", response_model=List[Analysis])
def get_all_analyses(repositories=Depends(database)):
    """Returns every analysis available"""
    return repositories["analysis"].all()


@router.get("/summary", response_model=List[AnalysisSummary])
def get_all_analyses_summaries(repositories=Depends(database)):
    """Returns a summary of every analysis within the application"""
    return repositories["analysis"].all_summaries()


@router.get("/{analysis_name}", response_model=Analysis)
def get_analysis_by_name(analysis_name: str, repositories=Depends(database)):
    """Returns analysis case data by calling method to find case by it's analysis_name"""
    return repositories["analysis"].find_by_name(analysis_name)


@router.post("/import", response_model=Analysis)
async def import_phenotips_json(
    background_tasks: BackgroundTasks,
    phenotips_input: BasePhenotips,
    repositories=Depends(database),
    annotation_task_queue=Depends(annotation_queue)
):
    """Imports the phenotips.json file into the database"""
    phenotips_importer = PhenotipsImporter(
        repositories["analysis"], repositories["genomic_unit"])
    try:
        new_analysis = phenotips_importer.import_phenotips_json(
            phenotips_input)
    except ValueError as exception:
        raise HTTPException(status_code=409) from exception

    analysis = Analysis(**new_analysis)
    annotation_service = AnnotationService(repositories["annotation_config"])
    annotation_service.queue_annotation_tasks(analysis, annotation_task_queue)
    background_tasks.add_task(AnnotationService.process_tasks,
                              annotation_task_queue, repositories['genomic_unit'])

    return new_analysis


@router.put("/update/{analysis_name}")
def update_analysis(analysis_name: str, analysis_data_changes: dict, repositories=Depends(database)):
    """Updates an existing analysis"""
    return repositories["analysis"].update_analysis(analysis_name, analysis_data_changes)


@router.put("/update_section/{analysis_name}")
def update_analysis_section(analysis_name: str, section_header: str, field_name: str,
                            updated_value: dict, repositories=Depends(database)):
    """Updates an existing analysis section by name, section header, and field name"""
    return repositories["analysis"].update_analysis_section(analysis_name, section_header, field_name, updated_value)


@router.post("/import_file", response_model=Analysis)
async def create_file(
    background_tasks: BackgroundTasks,
    phenotips_file: Union[bytes, None] = File(default=None),
    repositories=Depends(database),
    annotation_task_queue=Depends(annotation_queue)
):
    """ Imports a .json file for a phenotips case """
    # Quick and dirty json loads
    phenotips_input = BasePhenotips(**json.loads(phenotips_file))

    phenotips_importer = PhenotipsImporter(
        repositories["analysis"], repositories["genomic_unit"])
    try:
        new_analysis = phenotips_importer.import_phenotips_json(
            phenotips_input)
    except ValueError as exception:
        raise HTTPException(status_code=409) from exception

    analysis = Analysis(**new_analysis)
    annotation_service = AnnotationService(repositories["annotation_config"])
    annotation_service.queue_annotation_tasks(analysis, annotation_task_queue)
    background_tasks.add_task(AnnotationService.process_tasks,
                              annotation_task_queue, repositories['genomic_unit'])

    return new_analysis


@router.post("/upload/{analysis_name}")
def upload(analysis_name: str, upload_file: UploadFile = File(...), comments: str = Form(...),
           repositories=Depends(database)):
    """Uploads a file to GridFS and adds it to the analysis"""
    if repositories['bucket'].filename_exists(upload_file.filename):
        raise HTTPException(
            status_code=409, detail="File already exists in Rosalution")
    new_file_object_id = repositories['bucket'].save_file(
        upload_file.file, upload_file.filename)
    return repositories["analysis"].add_file(analysis_name, new_file_object_id, upload_file.filename, comments)


@router.get("/download/{file_id}")
def download_file_by_id(file_id: str, repositories=Depends(database)):
    """ Returns a file from GridFS using the file's id """
    grid_fs_file = repositories['bucket'].get_analysis_file_by_id(file_id)
    return StreamingResponse(grid_fs_file)


@router.get("/{analysis_name}/download/{file_name}")
def download(analysis_name: str, file_name: str, repositories=Depends(database)):
    """ Returns a file saved to an analysis from GridFS by file name """
    # Does file exist by name in the given analysis?
    file = repositories['analysis'].find_file_by_name(analysis_name, file_name)

    if not file:
        raise HTTPException(status_code=404, detail="File not found.")

    return StreamingResponse(repositories['bucket'].get_analysis_file_by_id(file['file_id']))


@router.post("/{analysis_name}/attach/pedigree")
def upload_pedigree(analysis_name: str, upload_file: UploadFile = File(...), repositories=Depends(database)):
    """ Specifically accepts a file to save a pedigree image file to mongo """
    new_file_object_id = repositories["bucket"].save_file(
        upload_file.file, upload_file.filename)

    return repositories["analysis"].add_pedigree_file(analysis_name, new_file_object_id)


@router.post("/{analysis_name}/attach/file")
def attach_supporting_evidence_file(
    analysis_name: str,
    upload_file: UploadFile = File(...),
    comments: str = Form(...),
    repositories=Depends(database)
):
    """Uploads a file to GridFS and adds it to the analysis"""
    if repositories['bucket'].filename_exists(upload_file.filename):
        raise HTTPException(
            status_code=409, detail="File already exists in Rosalution")
    new_file_object_id = repositories['bucket'].save_file(
        upload_file.file, upload_file.filename)
    return repositories["analysis"].attach_supporting_evidence_file(
        analysis_name, new_file_object_id, upload_file.filename, comments
    )


@router.post("/{analysis_name}/attach/link")
def attach_supporting_evidence_link(
    analysis_name: str,
    link_name: str = Form(...),
    link: str = Form(...),
    comments: str = Form(...),
    repositories=Depends(database)
):
    """Uploads a file to GridFS and adds it to the analysis"""
    return repositories["analysis"].attach_supporting_evidence_link(analysis_name, link_name, link, comments)


@router.get("/{analysis_name}/genomic_units")
def get_genomic_units(analysis_name: str, repositories=Depends(database)):
    """ Returns a list of genomic units for a given analysis """
    try:
        return repositories["analysis"].get_genomic_units(analysis_name)
    except ValueError as exception:
        raise HTTPException(
            status_code=404, detail=str(exception)) from exception


@router.delete("/{analysis_name}/attachment/{attachment_id}/remove")
def remove_supporting_evidence(analysis_name: str, attachment_id: str, repositories=Depends(database)):
    """ Removes a supporting evidence file from an analysis """
    if repositories["bucket"].id_exists(attachment_id):
        repositories["bucket"].delete_file(attachment_id)
    return repositories["analysis"].remove_supporting_evidence(analysis_name, attachment_id)

""" Analysis endpoint routes that serve up information regarding anaysis cases for rosalution """
import json

from typing import List, Union

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import StreamingResponse

from bson.errors import InvalidId

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


@router.get("/{name}", response_model=Analysis)
def get_analysis_by_name(name: str, repositories=Depends(database)):
    """Returns analysis case data by calling method to find case by it's name"""
    return repositories["analysis"].find_by_name(name)


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
        new_analysis = phenotips_importer.import_phenotips_json(phenotips_input)
    except ValueError as exception:
        raise HTTPException(status_code=409) from exception

    analysis = Analysis(**new_analysis)
    annotation_service = AnnotationService(repositories["annotation_config"])
    annotation_service.queue_annotation_tasks(analysis, annotation_task_queue)
    background_tasks.add_task(AnnotationService.process_tasks, annotation_task_queue, repositories['genomic_unit'])

    return new_analysis

@router.put("/update/{name}")
def update_analysis(name: str, analysis_data_changes: dict, repositories=Depends(database)):
    """Updates an existing analysis"""
    return repositories["analysis"].update_analysis(name, analysis_data_changes)

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
        new_analysis = phenotips_importer.import_phenotips_json(phenotips_input)
    except ValueError as exception:
        raise HTTPException(status_code=409) from exception

    analysis = Analysis(**new_analysis)
    annotation_service = AnnotationService(repositories["annotation_config"])
    annotation_service.queue_annotation_tasks(analysis, annotation_task_queue)
    background_tasks.add_task(AnnotationService.process_tasks, annotation_task_queue, repositories['genomic_unit'])

    return new_analysis

@router.post("/upload/{name}")
def upload(name: str, upload_file: UploadFile = File(...), comments: str = Form(...), repositories=Depends(database)):
    """Uploads a file to GridFS and adds it to the analysis"""
    if repositories['bucket'].check_if_exists(upload_file.filename):
        raise HTTPException(
            status_code=409, detail="File already exists in Rosalution")
    new_file_object_id = repositories['bucket'].save_file(
        upload_file.file, upload_file.filename)
    return repositories["analysis"].add_file(name, new_file_object_id, upload_file.filename, comments)

@router.get("/download/{file_id}")
def download_file_by_id(file_id: str, repositories=Depends(database)):
    gridFSFile = repositories['bucket'].get_analysis_file_by_id(file_id)
    return StreamingResponse(gridFSFile)

@router.get("/{analysis_name}/download/{file_name}")
def download(analysis_name: str, file_name: str, repositories=Depends(database)):
    """ Returns a file from GridFS by file name """
    # Does file exist by name in the given analysis?
    file = repositories['analysis'].find_file_by_name(analysis_name, file_name)

    if not file:
        raise HTTPException(status_code=404, detail="File not found.")
        
    return StreamingResponse(repositories['bucket'].get_analysis_file_by_id(file['file_id']))
    


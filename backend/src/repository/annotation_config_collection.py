"""
Manges the annotation configuration of various genomic units according to the
type of Genomic Unit.
"""
from distutils.command.config import config
from itertools import groupby

class AnnotationConfigCollection:
    """Repository for querying configurations for annotation"""

    def __init__(self, annotation_config_collection):
        """Initializes with the 'PyMongo' Collection object for the Data sets collection"""
        self.collection = annotation_config_collection

    def all(self):
        """Returns all annotation configurations"""
        return self.collection.find()

    def find_by_data_set(self, dataset_name):
        """Returns a data set source that matches by name"""
        return self.collection.findOne( { "data_set": dataset_name } )

    def datasets_to_annotate_by_type(self, types):
        """gets dataset configurations according to the types"""
        configuration = self.all()
        return [dataset for dataset in configuration if dataset["genomic_unit_type"] in types]

    def datasets_to_annotate_for_units(self, genomic_units_to_annotate):
        """
        Returns an dict which uses GenomicUnitType enumeration as a key with
        a value being the list of datasets configured to annotate for that type
        """
        types_to_annotate = set(map(lambda x: x["type"], genomic_units_to_annotate))

        datasets_to_annotate = self.datasets_to_annotate_by_type(types_to_annotate)

        configuration = {}
        for genomic_unit_type in types_to_annotate:
            configuration[genomic_unit_type] = []

        for dataset in datasets_to_annotate:
            type = dataset['genomic_unit_type']
            configuration[type].append(dataset)

        # Unsure why this wasn't working, keeping here for now
        # for key, group in groupby(datasets_to_annotate, lambda x: x["genomic_unit_type"]):
        #     configuration[key] = list(group)

        return configuration

""" Class to instantiate Annotation Units and support its functions"""


class AnnotationUnit:
    """ Annotation Unit Class that houses the Genomic Unit and its corresponding dataset """

    def __init__(self, genomic_unit, dataset):
        self.genomic_unit = genomic_unit
        self.dataset = dataset
        self.version = ""

    def get_genomic_unit(self):
        """Getter method"""
        return self.genomic_unit['unit']

    def get_dataset(self):
        """Getter method"""
        return self.dataset['data_set']

    def has_dependencies(self):
        """Checks if the annotation unit's dataset has dependencies"""
        return "dependencies" in self.dataset

    def get_missing_dependencies(self):
        """Returns dependencies of the dataset of the annotation unit"""
        missing_dependencies = []
        for dependency in self.dataset['dependencies']:
            if dependency not in self.genomic_unit:
                missing_dependencies = [dependency]

        return missing_dependencies
    
    def get_annotation_values_with_dependencies(self):
        """
        Returns the annotation values from the genomic unit collection
        for the annotation unit and missing dependencies
        """
        return ""
    
    def ready_for_annotation(self):
        """Checks for annotation unit is ready for annotation"""
        return True
    
    def not_ready_and_latest_for_annotation(self):
        """
        If annotation unit is not ready, checks if it should continue annotation or
        calls increment_delay_count and get_missing_dependencies before continuing
        """
        return ""

    def increment_delay_count(self):
        """Sets the delay count of the annotation unit"""
        delay_count = self.dataset['delay_count'] + 1 if 'delay_count' in self.dataset else 0
        self.dataset['delay_count'] = delay_count
        return

    def should_continue_annotation(self):
        """
        Checks if the annotation unit should continue annotation by calculating if 
        delay count of annotation unit within the queue is less than a magic number (10).
        """
        if self.dataset['delay_count'] < 10:
            return True
        return False

    def to_name_string(self):
        """
        Returns the annotation unit's genomic_unit and corresponding dataset.
        """
        return f"{self.get_genomic_unit} for {self.get_dataset}"

    def set_latest_version(self, version_details):
        """Sets the Annotation Unit with the version details"""
        self.version = version_details

    def version_exists(self):
        """Checks if the Annotation Unit is versioned or not"""
        if self.version == "":
            return True
        return False

    def is_version_latest(self):
        """Checks if the annotated Annotation Unit has the latest version or not"""
        # Once we are getting versions, latest will be initialized as False
        latest = True

        if self.version_exists():
            # code to be added to check if version is latest
            latest = True

        return latest

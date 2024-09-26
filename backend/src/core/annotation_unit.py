""" Class to instantiate Annotation Units and support its functions"""

import copy


class AnnotationUnit:
    """ Annotation Unit Class that houses the Genomic Unit and its corresponding dataset """

    def __init__(self, genomic_unit, dataset):
        self.genomic_unit = copy.deepcopy(genomic_unit)
        self.dataset = dataset
        self.version = ""

    def get_genomic_unit(self):
        """Returns 'unit' from genomic_unit"""
        return self.genomic_unit['unit']

    def get_dataset_name(self):
        """Return's the name of the dataset from the configuration"""
        return self.dataset['data_set']

    def get_dataset_source(self):
        """Returns the dataset's source"""
        return self.dataset['data_source']

    def get_dataset_version_type(self):
        """Returns the dataset's versioning type"""
        return self.dataset['versioning_type']

    def is_transcript_dataset(self):
        """Returns true if the dataset is for a transcript"""
        return 'transcript' in self.dataset

    def get_genomic_unit_type(self):
        """Return's 'genomic_unit_type' from dataset"""
        return self.dataset['genomic_unit_type']

    def get_genomic_unit_type_string(self):
        """Return's 'genomic_unit_type' from dataset"""
        return self.genomic_unit['type'].value

    def has_dependencies(self):
        """Checks if the annotation unit's dataset has dependencies"""
        return "dependencies" in self.dataset

    def get_dependencies(self):
        """Returns dependencies of the dataset of the annotation unit"""
        if self.has_dependencies():
            return self.dataset['dependencies']
        return []

    def get_missing_dependencies(self):
        """
        Returns missing dependencies of the dataset of the annotation unit 
        if they are missing from the genomic_unit
        """
        missing_dependencies = []

        if 'dependencies' not in self.dataset:
            return missing_dependencies

        for dependency in self.dataset['dependencies']:
            if dependency not in self.genomic_unit:
                missing_dependencies = [dependency]

        return missing_dependencies

    def conditions_met_to_gather_annotation(self):
        """
        Checks for annotation unit is ready for annotation
        and calls the assign_annotation_value_to_dependency() function if ready
        """
        missing_dependencies = self.get_missing_dependencies()
        return len(missing_dependencies) == 0

    def set_annotation_for_dependency(self, missing_dependency_name, dependency_annotation_value):
        """
        Assigns annotation value to the genomic unit's missing dependency
        """
        self.genomic_unit[missing_dependency_name] = dependency_annotation_value

    def should_continue_annotation(self):
        """
        If annotation unit is not ready, checks if it should continue annotation or
        calls increment_delay_count and get_missing_dependencies before continuing
        """
        self.increment_delay_count()

        return not self.delay_count_exceeds()

    def get_delay_count(self):
        """Returns the current annotation delay count"""
        return self.dataset['delay_count'] if 'delay_count' in self.dataset else 0

    def increment_delay_count(self):
        """Sets the delay count of the annotation unit"""
        delay_count = self.dataset['delay_count'] + 1 if 'delay_count' in self.dataset else 0
        self.dataset['delay_count'] = delay_count
        return

    def delay_count_exceeds(self):
        """
        Checks if the annotation unit has exceeded the delay count within the queue.
        Delay count is set as a magic number (10).
        """
        if self.dataset['delay_count'] < 10:
            return False
        return True

    def to_name_string(self):
        """
        Returns the annotation unit's genomic_unit and corresponding dataset.
        """
        return f"{self.get_genomic_unit()} for {self.get_dataset_name()}"

    def get_version(self):
        """
        Returns the version of this annotation unit, if none set, returns an empty string.
        """
        return self.version

    def set_latest_version(self, version_details):
        """Sets the Annotation Unit with the version details"""
        # This has not been implemented yet
        self.version = version_details

    def version_exists(self):
        """Checks if the Annotation Unit is versioned or not"""
        # This is currently a placeholder, and just returning True for now
        return self.version != ""

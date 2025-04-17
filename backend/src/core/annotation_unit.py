""" Class to instantiate Annotation Units and support its functions"""

import copy


class AnnotationUnit:
    """ Annotation Unit Class that houses the Genomic Unit and its corresponding dataset """

    def __init__(self, genomic_unit, dataset, analysis_name: str = ""):
        self.genomic_unit = copy.deepcopy(genomic_unit)
        self.dataset = dataset
        self.version = ""
        self.analysis_name = analysis_name

        self.transcript_provisioned = False

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

    def does_source_and_version_match(self, data_source, version):
        """Compares if an AnnotationUnit's """
        return self.get_dataset_source() == data_source and self.version == version

    def is_transcript_dataset(self):
        """Returns true if the dataset is for a transcript"""
        return 'transcript' in self.dataset

    def if_transcript_needs_provisioning(self):
        """
        Returns true if the dataset is a transcript, and will need
        'transcript_id' to already exist as an annotation
        """
        return self.is_transcript_dataset() and self.get_dataset_name() != "transcript_id"

    def set_transcript_provisioned(self, flag: bool):
        """Update the transcript dataset indicating whether it is ready for annotation"""
        self.transcript_provisioned = flag

    def is_transcript_provisioned(self):
        """Returns True when a Transcript dataset is transcript is provisioned to annotate."""
        return self.transcript_provisioned

    def get_genomic_unit_type(self):
        """Return's 'genomic_unit_type' from dataset"""
        return self.dataset['genomic_unit_type']

    def get_genomic_unit_type_string(self):
        """Return's 'genomic_unit_type' from dataset"""
        return self.genomic_unit['type'].value

    def has_dependencies(self):
        """Checks if the dataset is configured with dependencies"""
        return "dependencies" in self.dataset or self.is_transcript_dataset()

    def get_dependencies(self):
        """Returns dependencies of the dataset of the annotation unit"""
        return self.dataset['dependencies'] if 'dependencies' in self.dataset else []

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
                missing_dependencies.append(dependency)

        return missing_dependencies

    def conditions_met_to_gather_annotation(self):
        """
        Checks for annotation unit is ready for annotation
        and calls the assign_annotation_value_to_dependency() function if ready
        """
        missing_dependencies = self.get_missing_dependencies()
        conditions_list = [len(missing_dependencies) == 0]

        if self.if_transcript_needs_provisioning():
            conditions_list.append(self.is_transcript_provisioned())

        return all(conditions_list)

    def get_missing_conditions(self):
        """
        Queries the list of missing conditions that the AnnotationUnit needs meet in order to be ready for
        annotation. 
        """
        missing_conditions = [*self.get_missing_dependencies()]

        if self.if_transcript_needs_provisioning() and not self.is_transcript_provisioned():
            missing_conditions.append("transcript_id")
        return missing_conditions

    def set_annotation_for_dependency(self, missing_dependency_name, dependency_annotation_value):
        """
        Assigns annotation value to the genomic unit's missing dependency
        """
        self.genomic_unit[missing_dependency_name] = dependency_annotation_value

    def should_continue_annotation(self):
        """
        Checks if the annotation unit should continue to try and prepare for annotation. Each time the
        annotation unit checks if it should continue annotation, the delay count increases.  Once it has hit the
        magic number 10 for times checked to delay, it will return False.
        """
        delay_count = self.dataset['delay_count'] + 1 if 'delay_count' in self.dataset else 0
        self.dataset['delay_count'] = delay_count

        is_delay_count_exceeding = self.dataset['delay_count'] > 10

        return not is_delay_count_exceeding

    def set_latest_version(self, version_details):
        """Sets the Annotation Unit with the version"""
        self.version = version_details

    def version_exists(self):
        """Checks if the Annotation Unit is versioned or not"""
        return self.version != ""

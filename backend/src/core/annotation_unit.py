""" Class to instantiate Annotation Units and support its functions"""


class AnnotationUnit:
    """ Annotation Unit Class that houses the Genomic Unit and its corresponding dataset """

    def __init__(self, genomic_unit, dataset):
        self.genomic_unit = genomic_unit
        self.dataset = dataset

    def get_genomic_unit(self):
        """Getter method"""
        return self.genomic_unit['unit']

    def get_dataset(self):
        """Getter method"""
        return self.dataset['data_set']

    def get_missing_dependencies(self):
        """Returns dependencies of the dataset of the annotation unit"""
        missing_dependencies = []
        for dependency in self.dataset['dependencies']:
            if dependency not in self.genomic_unit:
                missing_dependencies = [dependency]

        return missing_dependencies

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

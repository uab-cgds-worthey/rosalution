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

    def set_delay_count(self):
        """Sets the delay count of the annotation unit"""
        delay_count = self.dataset['delay_count'] + 1 if 'delay_count' in self.dataset else 0
        self.dataset['delay_count'] = delay_count
        return

    def check_delay_count(self):
        """Checks if the delay count of annotation unit within the queue is less than a magic number"""
        if self.dataset['delay_count'] < 10:
            return True
        return False

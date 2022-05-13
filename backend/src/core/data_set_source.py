"""
Models Data Sets that are used to annotate genomic units.
"""
# pylint: disable=too-few-public-methods
from random import randint
import time
from pydantic import BaseModel

from ..enums import GenomicUnitType



class DataSetSource(BaseModel):
    """An annotation source that matches a data set with the type of data it is used to annotate and its source"""
    type: GenomicUnitType
    data_set: str
    data_source: str

    def annotate(self, unit):
        """Method placeholder for where HTTP Requests for annotation happens"""
        value = randint(0, 10)
        time.sleep(value)
        log_line = f"Slept: {value} - Fake annotation for {unit} for datasets {self.data_set} from {self.data_source}\n"
        with open("divergen-annotation-log.txt", mode="a", encoding="utf-8") as log_file:
            log_file.write(log_line)
        return log_line

"""
Models Data Sets that are used to annotate genomic units.
"""
# pylint: disable=too-few-public-methods
from random import randint
import time
from typing import Optional
from pydantic import BaseModel

from ..enums import GenomicUnitType



class DataSetSource(BaseModel):
    """An annotation source that matches a data set with the type of data it is used to annotate and its source"""
    type: GenomicUnitType
    data_set: str
    data_source: str
    url: Optional[str]
    query_param: Optional[str]
    attribute: Optional[str]

    def base_url(self, unit):
        return f"{self.url.replace(f'{{{self.type.value}}}', unit['unit'])};"

    def annotate(self, unit):
        """Method placeholder for where HTTP Requests for annotation happens"""
        value = randint(0, 10)
        with open("divergen-annotation-log.txt", mode="a", encoding="utf-8") as log_file:
            if(self.url is not None):
                log_line = f"Annotating {self.base_url(unit)}{self.query_param} and saving {self.attribute}\n"
            else:
                time.sleep(value)
                log_line = f"Slept: {value} - Fake annotation for {unit} for datasets {self.data_set} from {self.data_source}\n"
            log_file.write(log_line)
        return log_line

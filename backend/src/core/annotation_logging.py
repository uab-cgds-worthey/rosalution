""" Annotation logging helper - Provides useful and uniform functions to help with formatting annotation logging """

ANNOTATION_UNIT_PADDING = 75


def annotation_log_label():
    """
    Provides a label for logging in the annotation section to make it easier to search on.
    Changing this label will be uniform throughout the annotation section.
    """
    return 'Annotation:'


def annotation_unit_string(genomic_unit, data_set):
    """
    Provides a formatted string for logging that is consistent with {genomic_unit} for {dataset}.
    The string is padded to make the logs uniform and easier to read.
    """
    return f"{annotation_log_label()} {genomic_unit} for {data_set}".ljust(ANNOTATION_UNIT_PADDING)

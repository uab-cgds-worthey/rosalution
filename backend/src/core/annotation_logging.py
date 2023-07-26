annotation_unit_padding = 65

def annotation_log_label():
    return 'Annotation:'

def annotation_unit_string(genomic_unit, data_set):
    return f"{genomic_unit} for {data_set}".ljust(annotation_unit_padding)
import glob
import re


def fhir_resource_path(fhir_resource, parent_folder):
    # this is highly inefficient, since we need to scan the entire folder.
    # It might be interesting to cache the folder structure

    # case insensitive glob
    # source: https://medium.com/@tylercubell/python-case-insensitive-glob-80ba7306b327
    pattern = ".*/{}.yml".format(fhir_resource)
    matching_files = [file for file in glob.glob(f'../{parent_folder}/**', recursive=True) if re.match(pattern, file, flags=re.IGNORECASE)]
    if not matching_files:
        return None
    else:
        return matching_files[0]
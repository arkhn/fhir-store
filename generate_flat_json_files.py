import copy
import glob
import json
import os
import re

from itertools import combinations

RESOURCES = './resources'

# Collect datatypes
datatypes = {}

for filepath in glob.iglob('./resources/json/Datatypes/*.json', recursive=True):
    filename = os.path.splitext(os.path.basename(filepath))[0]

    with open(filepath, 'r') as datatype_file:
        datatypes[filename] = json.load(datatype_file)

# Collect Fhir resources
def replaceDatatypes(obj):
    returnObj = copy.copy(obj)

    r = re.compile(r"(.*)<(.*)>")

    for key in returnObj:
        result = r.match(key)
        if result:
            name, type = result.group(1), result.group(2)
            type = type.split('::')[1] if len(type.split('::')) > 1 else type

            if type in datatypes:
                returnObj[key] = datatypes[type]
                returnObj[key] = replaceDatatypes(returnObj[key])
            elif type == 'list':
                if returnObj[key]:
                    returnObj[key] = [
                        replaceDatatypes(returnObj[key][0])
                    ]

    return returnObj

resources = {}

for filepath in  glob.iglob('./resources/json/*/*/*.json', recursive=True):
    filename = os.path.splitext(os.path.basename(filepath))[0]
    resources[filename] = None

    with open(filepath, 'r') as resource_file:
        resource = json.load(resource_file)

    parsedResource = replaceDatatypes(resource)

    with open('./resources/flat_json/fhirResources/{}.json'.format(filename), 'w+') as f:
        f.write(json.dumps(parsedResource))

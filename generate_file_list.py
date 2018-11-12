import glob
import json
import os

from itertools import combinations

EXTENSIONS = ['json', 'yml']
RESOURCES = './resources'


lists = []

# List all available resources for all possible extensions
for extension in EXTENSIONS:
    list = []

    # Iterate through actual fhir resources
    resultDict = {}

    for filepath in glob.iglob('{}/{}/*/*/*.{}'.format(RESOURCES, extension, extension), recursive=True):
        path, filename = os.path.split(filepath)
        filename = os.path.splitext(filename)[0]

        usefulPath = path.split('/')[3:]

        resultDict[filename] = None

        list.append(filename)

    with open(os.path.join(RESOURCES, extension, 'resource_list.json'), 'w+') as f:
        f.write(json.dumps(resultDict))

    # Iterate through fhir datatypes
    resultDict = {}

    for filepath in glob.iglob('{}/{}/*/*.{}'.format(RESOURCES, extension, extension), recursive=True):
        path, filename = os.path.split(filepath)
        filename = os.path.splitext(filename)[0]

        usefulPath = path.split('/')[3:]

        resultDict[filename] = None

        list.append(filename)

    with open(os.path.join(RESOURCES, extension, 'datatypes_list.json'), 'w+') as f:
        f.write(json.dumps(resultDict))

    lists.append(list)
    print('Listed {} {} fhir resources appart from datatypes.'.format(len(list), extension))

# Assumes all lists are equal
for a, b in combinations(range(len(lists)), 2):
    for x in lists[a]:
        if x not in lists[b]:
            raise('error')
    for x in lists[b]:
        if x not in lists[a]:
            raise('error')

print('Comparison test passed.')

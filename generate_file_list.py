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
    for filepath in glob.iglob('{}/{}/*/*/*.{}'.format(RESOURCES, extension, extension), recursive=True):
        filename = os.path.splitext(os.path.basename(filepath))[0]
        list.append(filename)

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

# Outputs result dictionary to json file
resultDict = {}
for x in lists[0]:
    resultDict[x] = None

with open(os.path.join(RESOURCES, 'resource_list.json'), 'w+') as f:
    f.write(json.dumps(resultDict))

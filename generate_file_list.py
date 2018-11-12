import glob
import json
import os

EXTENSIONS = ['json', 'yml']
RESOURCES = './resources'


for extension in EXTENSIONS:
    with open(os.path.join(RESOURCES, extension, 'resource_list.json'), 'w+') as f:
        resultDict = {}

        for filepath in glob.iglob('{}/{}/*/*/*.{}'.format(RESOURCES, extension, extension), recursive=True):
            path, filename = os.path.split(filepath)
            filename = os.path.splitext(filename)[0]

            resultDict[filename] = None

        print('Listed {} {} fhir resources appart from datatypes.'.format(len(resultDict), extension))

        f.write(json.dumps(resultDict))

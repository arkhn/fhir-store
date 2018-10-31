import pytest
import os
import json

from process import clean_json
from process import json_to_yml

CLEAN_DATA_FOLDER = 'tests/data/clean'
CORRUPTED_DATA_FOLDER = 'tests/data/corrupted'
FILES = ['patient.json']


@pytest.fixture(scope="module",
                params=[os.path.join(CORRUPTED_DATA_FOLDER, filename) for filename in FILES])
def cleaned_json(request):
    return clean_json(request.param)


@pytest.fixture(scope="module")
def cleaned_yml(cleaned_json):
    return json_to_yml(json.loads(cleaned_json))


@pytest.fixture(scope="module",
                params=[os.path.join(CLEAN_DATA_FOLDER, filename) for filename in FILES])
def expected_json(request):
    return json.load(open(request.param))

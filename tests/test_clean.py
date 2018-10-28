import json


def test_clean_json(cleaned_json, expected_json):

    # assert cleaned json is a valid json file
    assert json.load(cleaned_json)

    # assert cleaned json is equal to expected output
    assert cleaned_json == expected_json










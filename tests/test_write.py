import os
from process import write

DOMAIN = 'domain_test'
SUBDOMAIN = 'subdomain_test'
RESOURCE = 'resource_test'


def test_write(cleaned_json, cleaned_yml):

    write(domain=DOMAIN, subdomain=SUBDOMAIN, resource=RESOURCE, format='json', file_data=cleaned_json)
    write(domain=DOMAIN, subdomain=SUBDOMAIN, resource=RESOURCE, format='yml', file_data=cleaned_yml)

    json_path = os.path.join(os.path.join(DOMAIN, SUBDOMAIN, RESOURCE + '.json'))
    yml_path = os.path.join(os.path.join(DOMAIN, SUBDOMAIN, RESOURCE + '.yml'))

    # assert file have been written properly
    assert open(json_path, 'w') == cleaned_json
    assert open(yml_path, 'w') == cleaned_yml

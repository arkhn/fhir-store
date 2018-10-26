import os
import errno


def write(domain, subdomain, resource, file_data, format):
    supporter_formats = ('yml', 'json')
    if format not in ('yml', 'json'):
        raise NotImplementedError('FHIR Store only supports formats', supporter_formats)

    filename = '{}/{}/{}/{}.{}'.format(format, domain, subdomain, resource, format)
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    with open(filename, "w") as f:
        f.write(file_data)

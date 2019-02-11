import re
import os
import json

GRAPHQL_COMMANDS_FOLDER = './graphql'

class Clean:
    @staticmethod
    def clean_json(filename, output_file=None):
        with open(filename) as input_file:

            input_file.readline()

            # Remove and store comments
            new_lines = []
            comments = []
            for line in input_file:
                l = line.split("//", 1)
                # remove empty lines, and remove \n
                if l[0] not in '         ':
                    new_lines.append(l[0].replace("\n", ""))
                    comments.append(l[1].replace("\n", "").strip() if len(l) >= 2 else '')

            # Handle [{ }] {} from FHIR convention
            lines = new_lines
            new_lines = []
            corindex = 0
            for i, line in enumerate(lines):
                # One line case [{ }]
                # espaces, guillemets, crochets, après
                m = re.match(
                    '''(\s*)\"([^"]*)\"\s*\:\s*\[\{\s*([^}]*)\s+\}\](,*)''',
                    line)
                if m is not None:
                    lll = '{}"{}<list::{}>$({}$)": null{}'.format(
                        m.group(1), m.group(2), m.group(3),
                        comments[i].replace("\"", "\\\""), m.group(4))
                    # print(lll)
                    new_lines.append(lll)
                    continue

                # One line case { }
                m = re.match('''(\s*)"([^"]*)"\s*:\s*{\s*([^}]*)\s+}(,*)''',
                             line)
                if m is not None:
                    lll = '{}"{}<{}>$({}$)": null{}'.format(
                        m.group(1), m.group(2), m.group(3),
                        comments[i].replace("\"", "\\\""), m.group(4))
                    # print(lll)
                    new_lines.append(lll)
                    continue

                # One line case { } / [{ }] exception with a \n in it
                m = re.match('''(\s*"[^"]*"\s*:\s*\[?{\s*[^"}\]\s]+)\s*$''', line)
                if m is not None:
                    # concat in a single line, by extending i+1 and not append to new_line
                    next_line = lines[i + 1]
                    m_next = re.match('''\s*(\w.*)$''', next_line)
                    lines[i + 1] = m.group(1) + m_next.group(1)
                    # also romove the line in comments
                    # del comments[corindex]
                    # corindex -= 1
                    continue

                # Multi line case [{ \n ... \n }]
                m = re.match('''(\s*)\"([^"]*)\"\s*\:\s*\[\{\s*''', line)
                if m is not None:
                    lll = '{}"{}<list>$({}$)": {}'.format(
                        m.group(1), m.group(2),
                        comments[i].replace("\"", "\\\""), '[{')
                    # print(lll)
                    new_lines.append(lll)
                    continue

                # default behavior
                new_lines.append(line)

            corindex += 1

            # Handle < > type extraction and codes handling
            lines = new_lines
            new_lines = []
            for i, line in enumerate(lines):
                match = re.match(
                    '''(\s*)"([^"]*)"\s*:\s*\[?"?<([^>]*)>"?\]?(,*)''', line)
                if match is not None:
                    given_type = match.group(3)
                    # Test if [ ] present
                    if re.match(
                            '''(\s*)"([^"]*)"\s*:\s*\["?<([^>]*)>"?\](,*)''',
                            line):
                        list_marker = 'list::'
                    else:
                        list_marker = ''

                    if given_type == 'code':  # We need to get the code options given in comments
                        comment = comments[i]
                        code_match = re.match(
                            '''[^|]*(\s[A-Za-z\-]+\s(?:\|\s[A-Za-z\-]+\s)+)[^|]*''',
                            comment)
                        if code_match is not None:
                            codes = code_match.group(1).strip().split(' | ')
                            given_type += '=' + '|'.join(codes)
                        # Sometimes there is no code options
                        # else:
                        #    raise TypeError('No code provided', match)

                    new_lines.append('{}"{}<{}{}>$({}$)": null{}'.format(
                        match.group(1), match.group(2), list_marker,
                        given_type, comments[i].replace("\"", "\\\""), match.group(4)))
                    continue
                else:
                    new_lines.append(line)

            # Rm bug lines
            lines = new_lines
            new_lines = []
            kill_me_lines = [
                'see information codes'
            ]
            for i, line in enumerate(lines):
                if line not in kill_me_lines:
                    new_lines.append(line)

            # Fix ',' errors at end of line
            lines = new_lines
            new_lines = []
            indents = []
            for i, line in enumerate(lines):
                match = re.match('''^(\s*).*''', line)
                indent = len(match.group(1))
                last_indent = indents[-1] if len(indents) > 0 else 0
                if last_indent <= indent:
                    if not ',' in line:
                        line += ','
                if last_indent != indent:
                    last_line = new_lines[i - 1]
                    if ',' in last_line:
                        new_lines[i - 1] = last_line.replace(',', '')

                new_lines.append(line)
                indents.append(indent)

            jj = json.loads('\n'.join(new_lines))

            fhirDataTypes = [
                'Address',
                'Annotation',
                'Attachment',
                'CodeableConcept',
                'Coding',
                'ContactDetail',
                'ContactPoint',
                'Contributor',
                'DataRequirement',
                'Dosage',
                'ElementDefinition',
                'HumanName',
                'Identifier',
                'ParameterDefinition',
                'Period',
                'Quantity',
                'Range',
                'Ratio',
                'Reference',
                'RelatedArtifact',
                'SampledData',
                'Signature',
                'Timing',
                'TriggerDefinition',
                'UsageContext'
            ]

            DATATYPES_PATH = './json/DataTypes'
            maxDepth = 0

            def recAttribute(key, tree, depth):
                node = dict({
                    'depth': depth
                })

                if (depth > 10):
                    print(depth, key)

                if key == "resourceType":
                    print('ALERT', tree, key, depth)
                    return tree

                isDataType = False
                isDataTypeList = False
                beginning = None

                # get comment
                match = re.match(
                    '''(.*)\$\((.*)\$\)''', key)
                if match is not None:
                    beginning = match.group(1)
                    comment = match.group(2)
                    node['comment'] = comment

                # get type
                match2 = re.match('''(.*)<(.*)>''', beginning if beginning is not None else key)
                if match2:
                    name = match2.group(1)
                    type = match2.group(2)

                    isDataType = type in fhirDataTypes

                    match3 = re.match('''list::(.*)''', type)
                    if match3:
                        datatype = match3.group(1)
                        isDataTypeList = datatype in fhirDataTypes
                        # else:
                        #     raise '{} not in fhirDataTypes'.format(datatype)
                else:
                    name = key
                    type = key

                node['name'] = name
                node['type'] = type

                if isDataType:
                    with open(os.path.join(DATATYPES_PATH, '{}.json'.format(type)), 'r') as datatype_file:
                        datatype_content = json.load(datatype_file)
                        node['attributes'] = {
                            'create': []
                        }
                        for key2 in datatype_content:
                            if key2 != "resourceType":
                                node['attributes']['create'].append(
                                    recAttribute(key2, datatype_content[key2], depth+1)
                                )
                elif isDataTypeList:
                    with open(os.path.join(DATATYPES_PATH, '{}.json'.format(datatype)), 'r') as datatype_file:
                        datatype_content = json.load(datatype_file)
                        node['attributes'] = {
                            'create': [
                                {
                                    'depth': depth+1,
                                    'name': '{}_0'.format(datatype),
                                    'type': datatype,
                                    'isProfile': True,
                                    'attributes': {
                                        'create': []
                                    }
                                }
                            ]
                        }
                        for key2 in datatype_content:
                            if key2 != "resourceType":
                                node['attributes']['create'][0]['attributes']['create'].append(
                                    recAttribute(key2, datatype_content[key2], depth+2)
                                )
                elif isinstance(tree, list):
                    node['attributes'] = {
                        'create': [recAttribute(key2, tree[0][key2], depth+1) for key2 in tree[0]]
                    }
                elif tree is not None:
                    node['attributes'] = {
                        'create' : [recAttribute(key2, tree[key2], depth+1) for key2 in tree]
                    }

                return node

            resource = dict()
            resource['attributes'] = {
                'create': []
            }
            for key in jj:
                if key == 'resourceType':
                    resource['name'] = jj[key]
                else:
                    resource['attributes']['create'].append(recAttribute(key, jj[key], 1))

            if (filename == 'process/../scrap_files/Identification/Individuals/Patient.json'):
                print(json.dumps(resource, indent=2))

            command_file = os.path.join(GRAPHQL_COMMANDS_FOLDER, os.path.basename(filename))
            if not os.path.exists(os.path.dirname(command_file)):
                os.makedirs(os.path.dirname(command_file))
            with open(command_file, 'w') as f:
                f.write(json.dumps(resource, indent=2))

            # print(allTypes)
            print()

            if output_file is not None:
                if not os.path.exists(os.path.dirname(output_file)):
                    os.makedirs(os.path.dirname(output_file))
                with open(output_file, 'w') as output_file:
                    output_file.write('\n'.join(new_lines))
            else:
                return '\n'.join(new_lines)

            return maxDepth

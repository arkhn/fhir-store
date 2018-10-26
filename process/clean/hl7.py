import re


def clean_json(filename, output_file=None):
    input_file = open(filename)
    input_file.readline()

    # Remove and store comments
    new_lines = ['{']
    comments = [None]
    for line in input_file:
        l = line.split("//", 1)
        # remove empty lines, and remove \n
        if l[0] not in '         ':
            new_lines.append(l[0].replace("\n", ""))
            comments.append(l[1] if len(l) >= 2 else None)

    # Handle [{ }] {} from FHIR convention
    lines = new_lines
    new_lines = []
    for i, line in enumerate(lines):
        # One line case [{ }]
        m = re.match('''(\s*)\"([^"]*)\"\s*\:\s*\[\{\s*([^}]*)\s+\}\](,*)''', line)
        if m is not None:
            new_lines.append('{}"{}<list::{}>": null{}'.format(m.group(1), m.group(2), m.group(3), m.group(4)))
            continue

        # One line case { }
        m = re.match('''(\s*)"([^"]*)"\s*:\s*{\s*([^}]*)\s+}(,*)''', line)
        if m is not None:
            new_lines.append('{}"{}<{}>": null{}'.format(m.group(1), m.group(2), m.group(3), m.group(4)))
            continue

        # One line case { } exception with a \n in it
        m = re.match('''(\s*"[^"]*"\s*:\s*{\s*[^"}\s]+)\s*$''', line)
        if m is not None:
            # concat in a single line, by extending i+1 and not append to new_line
            next_line = lines[i + 1]
            m_next = re.match('''\s*(\w.*)$''', next_line)
            lines[i + 1] = m.group(1) + m_next.group(1)
            # also romove the line in comments
            del comments[i]
            continue

        # Multi line case [{ \n ... \n }]
        m = re.match('''(\s*)\"([^"]*)\"\s*\:\s*\[\{\s*''', line)
        if m is not None:
            new_lines.append('{}"{}<list>": {}'.format(m.group(1), m.group(2), '[{'))
            continue
        else:
            new_lines.append(line)

    # Handle < > type extraction and codes handling
    lines = new_lines
    new_lines = []
    for i, line in enumerate(lines):
        match = re.match('''(\s*)"([^"]*)"\s*:\s*\[?"?<([^>]*)>"?\]?(,*)''', line)
        if match is not None:
            given_type = match.group(3)
            # Test if [ ] present
            if re.match('''(\s*)"([^"]*)"\s*:\s*\["?<([^>]*)>"?\](,*)''', line):
                list_marker = 'list::'
            else:
                list_marker = ''

            if given_type == 'code':  # We need to get the code options given in comments
                comment = comments[i]
                code_match = re.match('''[^|]*(\s[A-Za-z\-]+\s(?:\|\s[A-Za-z\-]+\s)+)[^|]*''', comment)
                if code_match is not None:
                    codes = code_match.group(1).strip().split(' | ')
                    given_type += '=' + '|'.join(codes)
                else:
                    raise TypeError('No code provided', match)

            new_lines.append('{}"{}<{}{}>": null{}'.format(match.group(1), match.group(2), list_marker, given_type, match.group(4)))
            continue
        else:
            new_lines.append(line)

    if output_file is not None:
        output_file = open(output_file, 'w')
        output_file.write('\n'.join(new_lines))
        output_file.close()
    else:
        return '\n'.join(new_lines)

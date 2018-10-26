import re


def clean_json(filename, output_file=None):
    input_file = open(filename)
    input_file.readline()

    # Remove comments
    new_lines = ['{']
    for line in input_file:
        l = line.split("//", 1)
        # remove empty lines, and remove \n
        if l[0] not in '         ':
            new_lines.append(l[0].replace("\n", ""))

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
            next_line = lines[i + 1]
            m_next = re.match('''\s*(\w.*)$''', next_line)
            lines[i + 1] = m.group(1) + m_next.group(1)
            continue

        # Multi line case [{ \n ... \n }]
        m = re.match('''(\s*)\"([^"]*)\"\s*\:\s*\[\{\s*''', line)
        if m is not None:
            new_lines.append('{}"{}<list>": {}'.format(m.group(1), m.group(2), '[{'))
            continue
        else:
            new_lines.append(line)

    # Handle < >
    lines = new_lines
    new_lines = []
    for line in lines:
        # Without "" (ex <boolean>)
        m = re.match('''(\s*)"([^"]*)"\s*:\s*<([^>]*)>(,*)''', line)
        if m is not None:
            new_lines.append('{}"{}<{}>": null{}'.format(m.group(1), m.group(2), m.group(3), m.group(4)))
            continue

        # With "" (ex "<date>")
        m = re.match('''(\s*)"([^"]*)"\s*:\s*"<([^>]*)>"(,*)''', line)
        if m is not None:
            new_lines.append('{}"{}<{}>": null{}'.format(m.group(1), m.group(2), m.group(3), m.group(4)))
            continue
        else:
            new_lines.append(line)

    if output_file is not None:
        output_file = open(output_file, 'w')
        output_file.write('\n'.join(new_lines))
        output_file.close()
    else:
        return '\n'.join(new_lines)

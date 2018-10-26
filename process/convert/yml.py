

def json_to_yml(dict_obj, indent=0, is_in_list=False, head=True):
    lines = []
    for key, obj in dict_obj.items():
        if not is_in_list:
            str_indent = ' '*4*indent
        else:
            assert indent > 0
            str_indent = ' '*4*(indent - 1) + '  - '
            is_in_list = False

        if obj is None:
            lines += ['{}{}:'.format(str_indent, key)]
        elif isinstance(obj, str):
            lines += ['{}{}: "{}"'.format(' '*4*indent, key, obj)]
        elif isinstance(obj, list):
            lines += ['{}{}:'.format(str_indent, key)]
            for o in obj:
                lines += json_to_yml(o, indent+1, is_in_list=True, head=False)
        elif isinstance(obj, dict):
            lines += ['{}{}:'.format(str_indent, key)]
            lines += json_to_yml(obj, indent+1, head=False)
    if head:
        return '\n'.join(lines)
    else:
        return lines

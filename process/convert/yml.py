

def json_to_yml(dict_obj, indent=0, is_in_list=False):
    for key, obj in dict_obj.items():
        if not is_in_list:
            str_indent = ' '*4*indent
        else:
            assert indent > 0
            str_indent = ' '*4*(indent - 1) + '  - '
            is_in_list = False
        if obj is None:
            print('{}{}:'.format(str_indent, key))
        if isinstance(obj, str):
            print('{}{}: "{}"'.format(' '*4*indent, key, obj))
        elif isinstance(obj, list):
            print('{}{}:'.format(str_indent, key))
            for o in obj:
                json_to_yml(o, indent+1, is_in_list=True)
        elif isinstance(obj, dict):
            print('{}{}:'.format(str_indent, key))
            json_to_yml(obj, indent+1)

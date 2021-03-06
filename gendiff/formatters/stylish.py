import gendiff.engine as diff_engine


def make_pretty(diff):
    def inner(diff_tree, space=2):
        output = []
        indent = ' ' * space
        for key in sorted(diff_tree.keys()):
            status, value = diff_tree[key]
            value = stringify(value)
            if status == diff_engine.CHANGED:
                output.append(
                    inner({key: (diff_engine.REMOVED, value[0])}, space))
                output.append(
                    inner({key: (diff_engine.ADDED, value[1])}, space))
            else:
                if isinstance(value, dict):
                    if status == diff_engine.NESTED:
                        value = inner(value, space + 4)
                    else:
                        value = inner(
                            {
                                k: (diff_engine.UNCHANGED, v)
                                for k, v in value.items()
                            }, space + 4)
                    value = '{\n' + value + '\n  ' + indent + '}'
                output.append(get_output_row(key, value, indent, status))
        return '\n'.join(output)
    return '{\n' + inner(diff) + '\n}'


def get_output_row(key, value, indent, status=None):
    if status == diff_engine.ADDED:
        return '{}+ {}: {}'.format(indent, key, value)
    elif status == diff_engine.REMOVED:
        return '{}- {}: {}'.format(indent, key, value)
    return '{}  {}: {}'.format(indent, key, value)


def stringify(value):
    if isinstance(value, bool):
        return {True: 'true', False: 'false'}[value]
    elif value is None:
        value = 'null'
    return value

# python 3.10 +
from dataclasses import dataclass
from inspect import cleandoc
import pickle
import yaml
import os


def run(command, printing:bool = True):
    command_type = type(command).__name__
    match command_type:
        case 'str':
            pass
        case 'list':
            command = ' '.join(command)
        case _:
            raise TypeError(
                cleandoc(
                    f'''
                    expected types of 'command' argument:
                        str, list
                    get:
                        {command_type}
                    '''
                )
            )

    if printing:
        os.system(command)
    else:
        return os.popen(command).read()


def init(path=os.getcwd()):
    os.chdir(path)
    print(path)
    if 'data' not in os.listdir():
        os.mkdir('data')


class NameExpectedError(Exception):
    @staticmethod
    def text(data):
        if isinstance(data, dict):
            name = 'dict'
        else:
            name = 'else'
        return open(f'error_messages/{name}.txt').read()


class UnsupportedExtensionError(Exception):
    pass


class BetterData:
    """
    @DynamicAttrs
    disabling pycharm "unresolved attribute" warnings
    """
    def __init__(self, data: dict, name: str = None):
        if name:
            data['name'] = name
        for key, val in data.items():
            vars(self)[key] = val

    def to_dict(self, name=True):
        if isinstance(name, str):
            vars(self)['name'] = name
        elif not name:
            vars(self).pop('name', None)
        return vars(self)


def dump(data, name: str = None):
    if not name:
        if isinstance(data, dict):
            if 'name' not in data.keys():
                raise NameExpectedError(NameExpectedError.text(data))
            name = data['name']
        else:
            if 'name' not in vars(data).keys():
                raise NameExpectedError(NameExpectedError.text(data))
            name = data.name
    extension = name.split('.')[-1]
    match extension:
        case 'pickle':
            pickle.dump(data, open(f'data/{name}', 'wb'))
        case 'yml':
            if not isinstance(data, dict):
                data = data.to_dict
            yaml.dump(data, open(f'data/{name}', 'w'))
        case _:
            raise UnsupportedExtensionError(
                "only 'pickle' and 'yml' extensions supported"
            )


def load(name: str, ins: str = 'bd'):  # ins = instance or type
    extension = name.split('.')[-1]
    match extension:
        case 'pickle':
            data = pickle.load(open(f'data/{name}', 'rb'))
            data.name = name
            return data
        case 'yml ':
            data = yaml.load(open(f'data/{name}', 'r').read(), Loader=yaml.Loader)
            data['name'] = name
            match ins.lower():
                case 'dict' | 'dc' | 'dct':
                    return data
                case 'bd' | 'betterdata':
                    return BetterData(data)
                case _:
                    raise TypeError("Only 'bd' and 'dct' instances supported")
        case _:
            raise UnsupportedExtensionError("only 'pickle' and 'yml' extensions supported")


def list_subtract(list_, blacklist):
    for i in blacklist:
        if i in list_:
            list_.remove(i)
    return list_


def isends(file, ext):
    return file[-len(ext):] == ext


def conc(a, b):
    if a[-1] == "\\":
        a = a[:-1]
    return '\\'.join([a, b])


def filename(path:str):
    return path.rsplit('\\', 1)[-1]


def rmdir(path:str):
    run(f'RMDIR "{path}" /S /Q')


def rm(string:str, to_remove):
    if isinstance(to_remove, str):
        to_remove = [to_remove]
    for i in to_remove:
        string = string.replace(i, '')
    return string

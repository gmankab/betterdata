'''
oooooooooo.   oooooooooo.
`888'   `Y8b  `888'   `Y8b
 888     888   888      888
 888oooo888'   888      888
 888    `88b   888      888
 888    .88P   888     d88'
o888bood8P'   o888bood8P'

'''


from dataclasses import dataclass
from inspect import cleandoc as cd
from pprint import pp
import urllib
import pickle
import sys
import os


@dataclass
class Requirements:
    folder = 'https://raw.githubusercontent.com/gmankab/betterdata/main/libs'
    list = [
        'forbiddenfruit_0-1-4.py'
    ]


sys.path.append('.')
if 'libs' in os.listdir():
    sys.path.append('.')


try:
    for requirement in Requirements.list:
        __import__(requirement)
except ImportError:
    print('downloadings libs...')

    if 'libs' not in os.listdir():
        os.mkdir('libs')

    for requirement in Requirements.list:
        urllib.urlretrieve(
            f'{Requirements.folder}/{requirement}',
            f'libs/{requirement}'
        )


@dataclass
class Version:
    # the betterdata library was written in this version of python,
    # on lower python versions it will not work
    python_required = '3.10.1'

    # stable work is guaranteed only on python versions listed here:
    python_tested_on = [
        '3.10.1'
    ]

    betterdata = '22.0'


@dataclass
class Contacts:
    telegram = 'https://t.me/gmanka'
    discord = 'gmanka#3806'
    github = 'https://github.com/gmankab/betterdata'


@dataclass
class Donate:
    DonationAlerts = 'https://donationalerts.com/r/gmanka'
    tinkoff = '5536 9139 9403 2981'
    sber = '5336 6903 8044 6684'


# noqa: E731
# noqa: F821
# pyright: reportUndefinedVariable=false
# pyright: reportMissingImports=false
# pylint: disable=import-outside-toplevel
# pylint: disable=import-error


def check_python_vers(required_vers):
    if '.'.join(str(i) for i in sys.version_info) < required_vers:
        raise VersionError(
            f'Python version must be at least {required_vers}'
        )


check_python_vers(required_vers=Version.python_required)


def to_list(*args, convert=None):
    '''
    make list of str from anything
    '''

    @dataclass
    class Answer:
        list = []

    def recursive_add_str(whatever):
        if isinstance(whatever, (list, tuple)):
            for i in whatever:
                recursive_add_str(i)
        else:
            if convert:
                whatever = convert(whatever)
            Answer.list.append(whatever)

    for arg in args:
        recursive_add_str(arg)

    return Answer.list


from forbiddenfruit import curse
import yaml


def modify_builtin_functions():
    def str_isends(self, end):
        return self[-len(end):] == end

    def str_conc(self, *peaces):  # universal analog of ".join()"
        return self.join(to_list(peaces, convert=str))

    def str_rm(self, *to_remove):
        to_remove = to_list(to_remove, convert=str)
        for i in to_remove:
            self = self.replace(i, '')
        return self

    def str_rmborders(self, *borders):
        for border in to_list(borders):
            while self[:len(border)] == border:
                self = self[len(border):]
            while self[-len(border):] == '\\':
                self = self[:-len(border)]

    def str_msplit(self, *delims, limit=None):
        if not limit and isinstance(delims[-1], int):
            limit = delims[-1]
            delims = delims[:-1]
        delims = to_list(delims)
        pos = 0
        splitted = []
        for index in range(len(self)):
            for delim in delims:
                if self[index:index + len(delim)] == delim:
                    if limit:
                        limit -= 1
                    elif limit == 0:
                        splitted.append(self[pos:])
                        return splitted
                    if self[pos:index]:
                        splitted.append(self[pos:index])
                    pos = index + len(delim)
        splitted.append(self[pos:])
        return splitted

    def list_rm(self, *to_remove):
        for i in to_list(to_remove):
            if i in self:
                self.remove(i)
        return self

    for funcname, func in locals().copy().items():
        builtin_funcname, addmethod = funcname.split('_', 1)
        curse(eval(builtin_funcname), addmethod, func)


modify_builtin_functions()


class VersionError(Exception):
    pass


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


class Bd:
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


class Path:
    def __init__(self, *peaces):
        peaces = to_list(peaces)
        self.list = []
        self.conc(peaces)
        # for i in args.split('/'):
        #     self.list += i.msplit()

    def __repr__(self) -> str:
        return self.str

    def __getitem__(self, item):
        return self.list[item]

    def conc(self, *peaces):
        peaces = to_list(peaces, convert=str)
        for peace in peaces:
            self.list += peace.msplit('/', '\\')
            self.str = '/'.join(self.list)
        return self.str

    def rmdir(self):
        run(f'rmdir "{self.str}" /S /Q')

    isends = str.isends


def run(command, printing: bool = True):
    command_type = typestr(command)
    match command_type:
        case 'str':
            pass
        case 'list':
            command = ' '.join(command)
        case _:
            raise TypeError(
                cd(
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
            data = yaml.load(
                open(f'data/{name}', 'r').read(),
                Loader=yaml.Loader
            )
            data['name'] = name
            match ins.lower():
                case 'dict' | 'dc' | 'dct':
                    return data
                case 'bd' | 'betterdata':
                    return Bd(data)
                case _:
                    raise TypeError("Only 'bd' and 'dct' instances supported")
        case _:
            raise UnsupportedExtensionError(
                "only 'pickle' and 'yml' extensions supported"
            )


def typestr(object_):  # type name
    return type(object_).__name__


def type_error_message(expected, get):
    return cd(
        f'''
        expected types:
            {', '.join(expected)}
        get:
            {get}
        '''
    )

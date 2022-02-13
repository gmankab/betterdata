'''
oooooooooo.   oooooooooo.
`888'   `Y8b  `888'   `Y8b
 888     888   888      888
 888oooo888'   888      888
 888    `88b   888      888
 888    .88P   888     d88'
o888bood8P'   o888bood8P'

GMANKA LICENSE
'''


# import only builtin libs
from dataclasses import dataclass
from genericpath import isdir
from itertools import islice
from inspect import cleandoc as cd
from pprint import pp
from urllib import request as r
import zipfile
import pathlib
import shutil
import pickle
import time
import sys
import os


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


def get_file_dir():
    return str(pathlib.Path(__file__).parent.resolve()).replace('\\', '/')


filedir = get_file_dir()


def install_libs(
    link: str,
    requirements: list,
    filedir = filedir,
    dir_name: str = 'bd_libs',
    path: str | bool = None,
    delete_zip: bool = True,
):
    if path:
        path = path.repace('\\', '/')
        dir_name = path.rsplit('/', 1)[-1]
    else:
        path = f'{filedir}/{dir_name}'

    sys.path.append(path)

    try:
        for requirement in requirements:
            __import__(requirement)
    except ImportError:

        while path in sys.path:
            sys.path.remove(path)
        print(sys.path)

        print('Downloading requirements for betterdata...')

        if isdir(path):
            shutil.rmtree(path)

        if not isdir(path):
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)

        zip_path = f'{path}/libs.zip'

        r.urlretrieve(
            link,
            filename = zip_path
        )

        zipfile.ZipFile(zip_path, 'r').extractall(path)
        if delete_zip:
            os.remove(zip_path)

        sys.path.append(path)

        print('Done.')


print(sys.path)

install_libs(
    dir_name = 'bd_libs',
    requirements = [
        'forbiddenfruit-0_1_4',
        'yml-6_0',
    ],
    link = (
        'https://github.com/gmankab/betterdata'
        '/raw/main/filehost/bd_libs-v1.zip'
    )
)

print(sys.path)

print(os.listdir(sys.path[-1]))
# import non-builtin libs
from forbiddenfruit_0_1_4 import curse
import yml_6_0 as yml


# noqa: E731
# noqa: F821
# noqa: F841
# pyright: reportUndefinedVariable=false
# pyright: reportMissingImports=false
# pyright: reportMissingModuleSource=false
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
        self.list = []
        peaces = to_list(peaces)
        self.conc(peaces)

    def __repr__(self) -> str:
        return self.to_str()

    def __getitem__(self, item):
        return self.list[item]

    def to_str(self):
        return '/'.join(self.list)

    def conc(self, *peaces):
        peaces = to_list(peaces, convert=str)
        for peace in peaces:
            self.list += peace.msplit('/', '\\')
        return self.to_str()

    def mkdir():
        if not isdir(dir):
            pathlib.Path(dir).mkdir(parents=True, exist_ok=True)

    def rmdir(self):
        if isdir(self.to_str()):
            shutil.rmtree(self.to_str())

    def rm(self):
        if os.path.isfile(self.to_str()):
            os.remove(self.to_str())

    def tree(
        self,
        level: int = -1,
        limit_to_directories: bool = False,
        length_limit: int = 1000,
    ):
        """
        Given a directory Path object print a visual tree structure
        This method is stolen from stack overflow
        https://stackoverflow.com/questions/9727673
        """
        space = '    '
        branch = '│   '
        tee = '├── '
        last = '└── '
        dir_path = pathlib.Path(self.to_str())
        files = 0
        directories = 0

        def inner(
            dir_path: Path,
            prefix: str = '',
            level=-1
        ):
            nonlocal files, directories
            if not level:
                return  # 0, stop iterating
            if limit_to_directories:
                contents = [d for d in dir_path.iterdir() if d.is_dir()]
            else:
                contents = list(dir_path.iterdir())
            pointers = [tee] * (len(contents) - 1) + [last]
            for pointer, path in zip(pointers, contents):
                if path.is_dir():
                    yield prefix + pointer + path.name
                    directories += 1
                    extension = branch if pointer == tee else space
                    yield from inner(
                        path,
                        prefix = prefix + extension,
                        level = level - 1
                    )
                elif not limit_to_directories:
                    yield prefix + pointer + path.name
                    files += 1
        result = dir_path.name
        iterator = inner(dir_path, level=level)
        for line in islice(iterator, length_limit):
            result += f'\n{line}'
        if next(iterator, None):
            result += f'\n... length_limit, {length_limit}, reached, counted:'
        result += f'\n\n{directories} directories'
        if files:
            result += f', {files} files'
        return result


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
            yml.dump(data, open(f'data/{name}', 'w'))
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
            data = yml.load(
                open(f'data/{name}', 'r').read(),
                Loader=yml.Loader
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


def update():
    (
        'https://raw.githubusercontent.com/gmankab/betterdata/'
        'main/filehost/latest_working_bd.py'
    )


update()

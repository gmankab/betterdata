'''
BETTERDATA
https://github.com/gmankab/betterdata

oooooooooo.   oooooooooo.
`888'   `Y8b  `888'   `Y8b
 888     888   888      888
 888oooo888'   888      888
 888    `88b   888      888
 888    .88P   888     d88'
o888bood8P'   o888bood8P'

GMANKA LICENSE
https://github.com/gmankab/licence
'''

# import only builtin libs
from dataclasses import dataclass
from itertools import islice
from inspect import cleandoc
from pprint import pp
from urllib import request as r
import pathlib
import shutil
import pickle
import time
import sys
import os


@dataclass
class Version:
    # version of betterdata
    betterdata = '22.0'

    # this version of betterdata was tested
    # only on python versions listed here:
    python_tested_on = [
        '3.10.2'
    ]

    # on lower python versions
    # betterdata will not work
    minimal_python = '3.10.0'


@dataclass
class Contacts:
    telegram = '@gmanka'
    discord = 'gmanka#3806'
    github = 'gmankab'


@dataclass
class Links:
    telegram  = 'https://t.me/gmanka'
    discord   = 'https://discord.com/users/396578935540023296'
    github    = 'https://github.com/gmankab/betterdata'
    license   = 'https://github.com/gmankab/licence'
    latest_bd = 'https://github.com/gmankab/betterdata/raw/main/latest_release/bd.py'
    libs      = 'https://github.com/gmankab/betterdata/raw/main/archive/bd_libs-v1.zip'


@dataclass
class Donate:
    DonationAlerts = 'https://donationalerts.com/r/gmanka'
    tinkoff = '5536 9139 9403 2981'
    sber    = '5336 6903 8044 6684'


def cp(path):
    '''
    clean path
    '''
    path = str(path).replace('\\', '/')
    while '//' in path:
        path = path.replace('//', '/')
    return path


def get_file_dir() -> str:
    return cp(pathlib.Path(__file__).parent.resolve())


FILEDIR = get_file_dir()


def install_libs(
    requirements: list,
    zip_name: str,
    link: str = None,
    folder_path: str = None,
    message_1: str = f'Downloading requirements for {os.path.basename(__file__)}...',
    message_2: str = 'Done. Restarting...',
) -> None:
    if folder_path:
        folder_path = cp(folder_path)
        if os.path.isdir(folder_path):
            raise FileExistsError(
f'''
Directory "{folder_path}" not  found.\n
Try specify other dir,
or don't specify it,
if you want to use your file folder
'''.cd()
            )
    else:
        folder_path = FILEDIR

    zip_path = f'{folder_path}/{zip_name}'
    sys.path.append(zip_path)

    try:
        for requirement in requirements:
            __import__(requirement)
    except ImportError as error:
        if not link:
            raise ModuleNotFoundError(
f'''
Error while importing "{requirement}" from {zip_path}:'
{error.msg}
'''.cd()
            ) from error

        print(message_1)

        if folder_path and not os.path.isdir(folder_path):
            pathlib.Path(folder_path).mkdir(parents=True, exist_ok=True)

        if os.path.isfile(zip_path):
            os.remove(zip_path)

        r.urlretrieve(
            link,
            filename = zip_path,
        )

        print(message_2)

        os.system(
            f'{sys.executable} {__file__}'
        )
        sys.exit()


install_libs(
    requirements = [
        'forbiddenfruit_0_1_4',
        'yml_6_0',
    ],
    zip_name='bd_libs.zip',
    link = Links.libs,
    message_1 = 'Downloading requirements for betterdata...'
)


# import non-builtin libs
from forbiddenfruit_0_1_4 import curse
import yml_6_0 as yml


def check_python_vers(required_vers):
    if '.'.join(str(i) for i in sys.version_info) < required_vers:
        raise VersionError(
            f'Python version must be at least {required_vers}'
        )


check_python_vers(required_vers=Version.minimal_python)


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

    def str_rmborders(self, *borders, rm_whitespaces = True):
        removed = True
        while removed:
            removed = False
            if rm_whitespaces:
                borders += (' ', '\n')
            for border in to_list(borders):
                length = len(border)
                while self[:length] == border:
                    self = self[length:]
                    removed = True
                while self[-length:] == border:
                    self = self[:-length]
                    removed = True
        return self

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

    def str_cd(
        self: str,
        tabs: int = 0,
        tab_symbol = ' ' * 4,
    ):
        '''
        Clean doc strings.
        Removes tabs before doc strings
        '''
        doc = cleandoc(self)
        if tabs:
            tab = '\n' + tab_symbol * tabs
            doc = tab + tab.join(doc.split('\n'))
        return doc

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

    def mkdir(self):
        if not os.path.isdir(self):
            pathlib.Path(self).mkdir(parents=True, exist_ok=True)

    def rmdir(self):
        if os.path.isdir(self.to_str()):
            shutil.rmtree(self.to_str())

    def rm(self):
        if os.path.isfile(self.to_str()):
            os.remove(self.to_str())

    def tree(
        self,
        level: int = -1,
        limit_to_directories: bool = False,
        length_limit: int = 1000,
        ignore: list = [],
        md_diff: bool = False,
        after_dir = '/'
    ):
        """
        Print a visual tree structure for given dir
        This method is stolen from stack overflow
        https://stackoverflow.com/questions/9727673
        But I rewrote it a bit.
        """
        branch = '│   '
        tee    = '├── '
        last   = '└── '
        plus   = '+ ' if md_diff else ""
        big_space  = ' ' * 4
        little_space = ' ' * 2 if md_diff else ""
        dir_path = pathlib.Path(self.to_str())
        files = 0
        directories = 0

        def inner(
            dir_path: pathlib.Path,
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
            for content in contents:
                for i in ignore:
                    if i in str(content):
                        while content in contents:
                            contents.remove(content)
            pointers = [tee] * (len(contents) - 1) + [last]
            for pointer, path in zip(pointers, contents):
                if path.is_dir():
                    yield plus + prefix + pointer + path.name + after_dir
                    directories += 1
                    extension = branch if pointer == tee else big_space
                    yield from inner(
                        path,
                        prefix = prefix + extension,
                        level = level - 1
                    )
                elif not limit_to_directories:
                    yield little_space + prefix + pointer + path.name
                    files += 1
        result = plus + dir_path.name + after_dir
        if md_diff:
            result = '```diff\n' + result
        iterator = inner(dir_path, level=level)
        for line in islice(iterator, length_limit):
            result += f'\n{line}'
        if next(iterator, None):
            result += f'\n... length_limit, {length_limit}, reached, counted:'
        if md_diff:
            result += '\n```'
        result += f'\n\n{directories} directories'
        if files:
            result += f', {files} files'
        return result


def run(commands, silent: bool = False):
    commands = to_list(commands)
    if not silent:
        for command in commands:
            os.system(command)
        return True

    answer = []
    for command in commands:
        answer.append(os.popen(command).read())
    if len(answer) == 1:
        return answer[0]

    return answer


def check_for_update():
    pass  # TODO

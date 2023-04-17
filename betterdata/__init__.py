# license: gnu gpl 3 https://gnu.org/licenses/gpl-3.0.en.html
# sources: https://github.com/gmankab/betterdata

from easyselect import Sel
from pathlib import Path
import gmanka_yml as yml
from rich import (
    pretty,
    traceback,
)
import rich
import sys


yes_no = Sel(
    items = [
        'yes',
        'no',
        'exit'
    ],
    styles = [
        'green',
        'red',
        'bright_black'
    ]
)


pretty.install()
traceback.install(
    show_locals=True
)
c = rich.console.Console()
print = c.print
version = '23.0.0'


class Data:
    # pylint: disable=no-member
    '''
    @DynamicAttrs
    '''
    def __init__(
        self,
        data: dict = {},
        path: str | Path | None = None,
    ) -> None:
        self.data = {}
        self.path = None
        self.set_data(
            data = data,
            path = path,
        )
        if (
            not self.data
        ) and (
            self.path
        ) and (
            self.path.exists()
        ):
            self.read_file()

    def __repr__(self) -> dict:
        return self.data

    def __str__(self) -> str:
        return str(self.data)

    def __getitem__(
        self,
        item,
    ):
        if item in self.data:
            return self.data[item]
        else:
            return None

    def __setitem__(
        self,
        key,
        val,
    ) -> None:
        self.data[key] = val
        vars(self)[key] = val
        self.to_file()

    def __add__(
        self,
        additional,
    ) -> dict:
        return self.data + additional

    def __contains__(
        self,
        item,
    ) -> bool:
        return item in self.data

    def set_data(
        self,
        data: dict | None = None,
        path = None
    ):
        if not data:
            data = {}
        if not isinstance(
            data,
            dict,
        ):
            raise TypeError(
                f'expected dict but {type(data)} got'
            )

        if path:
            self.path = Path(path)
        if data:
            self.data = data
            for key, val in data.items():
                vars(self)[key] = val
            self.to_file()

    def to_str(
        self
    ):
        return yml.to_str(
            data = self.data
        )

    def read_file(
        self,
        path = None,
    ):
        self.set_data(
            path = path,
        )
        self.set_data(
            data = yml.from_file(
                path = self.path
            )
        )

    def to_file(
        self,
        path = None
    ):
        self.set_data(
            path = path
        )
        if self.path and self.data:
            yml.to_file(
                data = self.data,
                path = self.path,
            )

    def interactive_input(
        self,
        item: str,
        digits_to_int: bool = True,
        skip_if_exist: bool = True,
        kill_app_on_exit: bool = True,
        confirm: bool = True,
        sel: Sel = yes_no,
        text = None,
    ):
        if skip_if_exist and self[item]:
            return

        while True:
            if text:
                print(text)
            else:
                print(f'\n[bold]input {item}:')
            try:
                val = input()
            except EOFError:
                continue
            if not val:
                continue

            if confirm:
                match sel.choose(
                    f'[deep_sky_blue1]{val}[/deep_sky_blue1] - is it correct?'
                ):
                    case 'no':
                        continue
                    case 'exit':
                        if kill_app_on_exit:
                            sys.exit()
                        else:
                            return
                    case 'yes':
                        pass
            if digits_to_int and val.isdigit():
                val = int(val)
            self[item] = val
            if self.path:
                self.to_file()
                print(f'[green]{item} saved to config:\n[deep_sky_blue1]{self.path}')
            return

    def print(
        self
    ):
        c.print(
            self.data
        )

# betterdata by gmanka

<img src="https://github.com/gmankab/betterdata/raw/main/img/transparent.png">

library for working with data. Features: automatic writing to disk when new data is added to an object, quick export to yml

## navigation

- [installation](#installation)
- [usage](#usage)
- [reading](#reading)
- [autosaves](#autosaves)
- [manual saves](#manual-saves)
- [some syntax sugar](#some-syntax-sugar)
- [interactive input](#interactive-input)
- [license](#license)

### installation[^](#navigation)

```sh
pip install betterdata
```

### usage[^](#navigation)

```py
from betterdata import Data

df = Data(
    data = {
        'key1': 'val1',
        'key2': 'val2',
    },
    file_path = 'data.yml'
)
```

after running this code it will automatically create file `data.yml`

```yml
key1: val1
key2: val2
```

if file already exists, then it will be overwritten

### reading[^](#navigation)

if you will not specify `data` argument, then data will be read from disk

```py
from betterdata import Data

df = Data(
    file_path = 'data.yml'
)

print(df)
# {'key1': 'val1', 'key2': 'val2'}
```

if file does not exists then dict will be empty

```py
from betterdata import Data
from pathlib import Path

Path('data.yml').unlink()

data = Data(
    file_path = 'data.yml'
)

print(data)
# {}
```

### autosaves[^](#navigation)

if you put something in the dictionary then it will also automatically written to disk

```py
from betterdata import Data

data = Data(
    file_path = 'data.yml'
)

print(data)
# {}
print(Path('data.yml').exists())
# False

data['key1'] = 'val1'
data['key2'] = 'val2'

print(data)
# {'key1': 'val1', 'key2': 'val2'}
print(open('data.yml', 'r').read())
# key1: val1
# key2: val2
```

### manual saves[^](#navigation)

if you editing list in a dict then it will not automatically saved, but you can save it manually

```py
from betterdata import Data
from pathlib import Path

Path('data.yml').unlink(missing_ok=True)
data = Data(
    file_path = 'data.yml'
)

print(data)
# {}
print(Path('data.yml').exists())
# False

data['list'] = [1, 2, 3]

print(data)
# {'list': [1, 2, 3]}
print(open('data.yml', 'r').read())
# list:
# - 1
# - 2
# - 3

data['list'].append('some very important data')

print(data)
# {'list': [1, 2, 3, 'some very important data']}
print(open('data.yml', 'r').read())
# list:
# - 1
# - 2
# - 3

# as you can see, appended data was not written on disk, so you can write it manually

data.to_file()

print(open('data.yml', 'r').read())
# list:
# - 1
# - 2
# - 3
# - some very important data
```

### some syntax sugar[^](#navigation)

```py
from betterdata import Data

data = Data(
    {
        'key1': 'val1',
        'key2': 'val2',
    }
)

print(data)
# {'key1': 'val1', 'key2': 'val2'}

print(data['key1'])
# val1

print(data.key1)
# val1

print(data.to_str())
# key1: val1
# key2: val2

print('key2' in data)
# True

print('key3' in data)
# False

print(data['key3'])
# None

print(data.key3)
# AttributeError: 'Data' object has no attribute 'key3'
```

### interactive input[^](#navigation)

```py
from betterdata import Data

data = Data()

data.interactive_input('key1')
```

it will interactively ask user to input value for `key1`

args:  
`item: str` # key name  
`digits_to_int: bool = True` # convert digits from str to int  
`kill_app_on_exit: bool = True` # kill app if user select `exit` button  
`break_if_exist: bool = True` # skip   interactive input if key already in dict  
`sel: Sel = yes_no` # you can specify Sel object from [easyselect lib](https://github.com/gmankab/easyselect) which will be used to confirm the value  
`text = None` # change text which will be printed on the screen

### license[^](#navigation)

[gnu gpl 3](https://gnu.org/licenses/gpl-3.0.en.html)

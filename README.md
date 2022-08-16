# Python Compiler
## what is Pypiler?

the pypiler project was created to facilitate the compilation of a
python script without major difficulties. It basically converts your
python code to c (using cython) and then compiles that c code as c
code normally.

> [OBS] cython is a requirement for the tool, but if you don't have it,
> will be installed automatically, if the "``install_cython``" key is set to ``true``

## how to install

- <a href="https://github.com/Jefferson5286/pypiler/releases/tag/pypiler">Download</a>

To install it, just download the rar file and extract it along with your project file, all its dependencies are already included in it, which
would be the clear compiler (mingw64) and python includes and
libs needed for compilation.

Python of course it is necessary but probably if you want to convert
your python code to executable you must have a python interpreter
(cpython) installed.

## how to use

### creating spec files:
First open your terminal in your project folder and run

````shell
python pypiler/pypiler.py init
````

After that, a json file will be created, with some information needed 
for the construction, but the really important ones are:
``install_cython``, ``name`` and ``target_python_file`` (for more 
information on pypiler.json check its [documention](#json pypiler properties).

### Compiling from Pypiler

By default, it is already a preset, but you can change it. First in 
``name`` put the name you want the executable to have, then after that
change ``target_python_file`` to the python file you want to create the
executable.

already in ``cython install``change to ``true`` if you don't have cython
in your python, it will be installed for you when compiling. otherwise
set to ``false`` so the installation of cython will be ignored.

done that you are now ready to compile your python file. Run this in 
your terminal.

> [OBS] ``-v`` is just for you to see what happens.
````shell
python pypiler/pypiler.py -v build pypiler.json
````

This does all the work for you, so if nothing goes wrong, you'll have
.exe and .c files in your directory! The .c is useless there so you can
delete it.

## about your project's dependencies
### your dependencies

Your modules and packages, images, etc. They must be next to the 
executable, the import system and directories will work as if it were
the same file.py.

### dependency on third-party modules

Well if you installed this module via pip you will need to leave this
module or package next to your executable without even a venv type, 
this will be fixed in the future so you don't have to worry about it.
I suggest you save all these modules in a folder called eg "dependencies",
like a python package, then import your code as if everything were one
big python package, eg: ``from dependencies.pygame import *``

### exemple

````json5
- root
    - assets
        player.png
    - dependencies
        - pygame
    - MyPackages
        - entities
        - objects
    - MyModule.py
    - MyApp.exe
````

## json pypiler properties

|        Name        |    Type    |                                         description                                        |
|:------------------:|:----------:|:------------------------------------------------------------------------------------------:|
| name               | ``string`` | name that will be used in the executable                                                   |
| target_python_file | ``string`` | python file to be compiled                                                                 |
| c_compiler         | ``string`` | compilador c ou c++ que será usado para compilar, são executáveis em "pypiler/mingw64/bin" |
| python_version     |   ``int``  | not yet enabled for changes, do not change its value                                       |
| remove_c_file      | ``bolean`` | if to remove c file created by cython                                                      |
| install_cython     | ``bolean`` | if you don't have cython installed set it to true for it to be installed                   |

---

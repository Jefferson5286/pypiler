from os import path, system, remove
from sys import argv
from json import dump, load


def init():
    obj = {
        "name": "MyApp",
        "target_python_file": "main.py",
        "python_version": 310,
        "c_compiler": "gcc",
        "remove_c_file": False,
        "install_cython": True
    }

    with open('pypiler.json', 'w', encoding='UTF-8') as _:
        dump(obj, _, indent=2)


class Build:
    def __init__(self, **kwargs):
        self.verbose = kwargs.get('verbose')
        spec = kwargs.get('spec')

        with open(spec, 'r', encoding='UTF-8') as _:
            properties = load(_)

        self.log('\ngetting specs in pypiler.json', self.verbose)
        self.exe_name = properties.get('name', 'MyApp')
        self.target = properties.get('target_python_file', 'main.py')
        self.pyv = properties.get('python_version', 310)
        self.compiler = properties.get('c_compiler', 'gcc')
        self.remove_c_cache = properties.get('remove_c_file', False)

        if properties.get('install_cython'):
            print('     [INFO] checking if python is installed, if not it will be installed for you :-)\n')
            system('pip install cython')

        self.log('checking user relative directory', self.verbose)
        self.user = path.expanduser('~')

        self.log('fetching includes do e libs python {self.pyv}', self.verbose)
        self.python = {
            'libs': f'{self.user}\\AppData\\Local\\Programs\\Python\\Python{self.pyv}\\libs',
            'includes': f'{self.user}\\AppData\\Local\\Programs\\Python\\Python{self.pyv}\\include'
        }

        self.log('creating path to a c file', self.verbose)
        self.c_cache = self.target.replace('.py', '.c')

        self.commands = {
            'cythonizer': f'cython -3 {self.target} --embed',
            'pyx_error': self.reformate_c_file,
            'compile':
                f'pypiler\\mingw64\\bin\\{self.compiler}.exe {self.c_cache} -I pypiler\\python\\include'
                f' -L pypiler\\python\\libs -l python{self.pyv} -o {self.exe_name}.exe',
            'execute': f'.\\{self.exe_name}'
        }

        self.run()

    @staticmethod
    def log(info, verbose) -> None:
        if verbose:
            print(f'     [INFO] {info}')

    def reformate_c_file(self) -> None:
        self.log(f'refactoring file {self.c_cache} fixing <__pyx_check_sizeof_voidp> error', self.verbose)
        with open(self.c_cache, 'r', encoding='UTF-8') as f:
            font = f.read() \
                .replace('enum { __pyx_check_sizeof_voidp = 1 / (int)(SIZEOF_VOID_P == sizeof(void*)) };', '') \
                .replace('int wmain(int argc, wchar_t **argv) {', 'int main(int argc, wchar_t **argv) {')

        with open(self.c_cache, 'w', encoding='UTF-8') as f:
            f.write(font)

    def run(self) -> None:
        self.log(f'cythonizer: {self.target}', self.verbose)
        system(self.commands['cythonizer'])

        self.commands['pyx_error']()

        self.log(f'compiling c code with the compiler {self.compiler}', self.verbose)
        system(self.commands['compile'])

        if self.remove_c_cache:
            self.log('removing c file', self.verbose)
            remove(self.c_cache)

        self.log('build process terminated!', self.verbose)


if argv[-1] == 'init':
    try:
        init()
        print('pypiler file built successfully!')
    except Exception as e:
        print('there was an error when creating the specification file, try again or create it manually, here is the '
              'documentation on how to create it')
        print(f'Error occurred: {e}')

elif argv[-2] == 'build':
    Build(verbose=True if '-v' in argv else False,
          spec=argv[-1])

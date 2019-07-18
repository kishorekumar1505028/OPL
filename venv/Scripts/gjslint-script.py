#!F:\1505028\MyDjangoProject\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'closure-linter==2.3.19','console_scripts','gjslint'
__requires__ = 'closure-linter==2.3.19'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('closure-linter==2.3.19', 'console_scripts', 'gjslint')()
    )

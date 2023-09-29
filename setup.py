import cx_Freeze
import sys
import os 
base = None

if sys.platform == 'win32':
    base = "Win32GUI"


PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')


executables = [cx_Freeze.Executable("inward.py", base=base, icon="logo.ico")]

cx_Freeze.setup(
    name="INWARD System",
    options={
        "build_exe": {
            "packages": ['os', 'pandas','numpy', 're', 'csv', 'logging', 'qdarkstyle', 'pymysql', 'datetime', 'sys'],
            "include_files": ["logo.ico", "logs", 'tcl86t.dll', 'tk86t.dll', 'Companyname.txt', "inward.sql", 'inward.ui', 'Location.txt', 'login.ui', 'logo.png', 'new.ui', 'search.txt', 'uom.txt','Database'],
            "excludes": [],  # Exclude NumPy from freezing
        },
    },
    version="1.0",
    description="INWARD System | Developed By Technic Corporation And Team",
    executables=executables
)

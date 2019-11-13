import py_compile

py_compile.compile(file='client_old.py', cfile="client.pyc", optimize=-1)
py_compile.compile(file='client_old.py', cfile="client.pyo", optimize=1)

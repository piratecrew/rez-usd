# -*- coding: utf-8 -*-

name = 'usd'

version = '20.11'

authors = ['frbr']

build_requires = [
    "Jinja2-2",
    "cmake-3+",
    "devtoolset-7",
    "~PySide2-5",
    "PyOpenGL-3"
]

@late()
def requires():
    result = []
    if in_context() and "PySide2" in request:
        result.append("PyOpenGL-3")
    return result

variants = [
    ["platform-linux", "python-2.7", "!PySide2"],
    ["platform-linux", "python-2.7", "PySide2-5"],
    ["platform-linux", "python-3.7", "!PySide2"],
    ["platform-linux", "python-3.7", "PySide2-5"],
]

hashed_variants = True

build_command = "bash {root}/build_usd.sh"

def commands():
    env.PYTHONPATH.append("{root}/lib/python")
    env.PATH.prepend("{root}/bin")
    if building:
        env.USD_DEPENDENCIES_ROOT.append("{base}/USD-Dependencies/{resolve.platform.version}/python-{resolve.python.version.major}")

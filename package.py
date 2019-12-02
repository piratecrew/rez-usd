# -*- coding: utf-8 -*-

name = 'usd'

version = '19.11'

authors = ['frbr']

build_requires = [
    "Jinja2-2",
    "cmake-3+",
    "devtoolset-7",
    "~PySide-2|5",
    "PyOpenGL-3"
]

@late()
def requires():
    result = []
    if in_context() and "PySide" in request:
        result.append("PyOpenGL-3")
    return result

variants = [
    ["platform-linux", "python-2.7", "!PySide"],
    ["platform-linux", "python-2.7", "PySide-2"],
]

hashed_variants = True

build_command = "bash {root}/build_usd.sh"

def commands():
    env.PYTHONPATH.append("{root}/lib/python")
    env.PATH.prepend("{root}/bin")
    if building:
        env.USD_DEPENDENCIES_ROOT.append("{base}/USD-Dependencies/{resolve.platform.version}")

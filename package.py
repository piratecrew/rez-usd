# -*- coding: utf-8 -*-

name = 'usd'

version = '0.8.0'

authors = ['fredrik.brannbacka']

build_requires = [
	"cmake-3",
]

requires = [
	"boost-1",
	"tbb-4",
	"openexr-2.2",
	"oiio-1",
	"glew-2",
	"opensubdiv",
	"PySide-1.2",
	"PyOpenGL",
	"Jinja2"
]

@early()
def variants():
    from rez.package_py_utils import expand_requires
    requires = ["platform-**", "os-*.*", "python-2.7"]
    return [expand_requires(*requires)]

def commands():
    env.PATH.prepend("{root}/bin")
    env.LD_LIBRARY_PATH.append("{root}/lib")
    env.PYTHONPATH.prepend("{root}/lib/python/")
# -*- coding: utf-8 -*-

name = 'usd'

version = '0.8.0'

authors = ['fredrik.brannbacka']

build_requires = [
	"cmake-3",
	"pyside_tools"
]

requires = [
	"boost-1",
	"tbb-4",
	"openexr-2.2",
	"oiio-1",
	"glew-2",
	"opensubdiv",
	"pyside-1",
	"PyOpenGL",
	"Jinja2",
	"maya-2017"
]

def commands():
    env.PATH.prepend("{root}/bin")
    env.LD_LIBRARY_PATH.append("{root}/lib")
    env.PYTHONPATH.prepend("{root}/lib/python/")
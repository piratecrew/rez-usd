# -*- coding: utf-8 -*-

name = 'usd'

version = '19.07'

authors = ['frbr']

build_requires = [
    "python-2.7",
    "PySide-2",
    "Jinja2-2",
    "PyOpenGL-3",
    "virtualenv",
    "cmake-3+",
    "devtoolset-7",
]

requires = [
    "python-2.7",
    "PySide-2",
    "Jinja2-2",
    "PyOpenGL-3",
]

variants = [
    ["platform-linux"],
    ["platform-linux", "renderman-22.6"],
    ["platform-linux", "maya-2018"],
    ["platform-linux", "maya-2019"]
]

build_command = "bash $REZ_BUILD_SOURCE_PATH/build_usd.sh; cp -r $REZ_BUILD_SOURCE_PATH/cmake $REZ_BUILD_INSTALL_PATH/"

def commands():  
    if "maya" in resolve:
        env.MAYA_PLUG_IN_PATH.append('{root}/third_party/maya/plugin')
        env.MAYA_SCRIPT_PATH.append('{root}/third_party/maya/lib/usd/usdMaya/resources')
        env.MAYA_SCRIPT_PATH.append('{root}/third_party/maya/plugin/pxrUsdPreviewSurface/resources')
        env.PYTHONPATH.append('{root}/lib/python')
        env.XBMLANGPATH.append('{root}/third_party/maya/lib/usd/usdMaya/resources')
    elif "houdini" in resolve:
        env.HOUDINI_PATH.append('{root}/third_party/houdini')
        env.HOUDINI_DSO_ERROR = 1
        env.HOUDINI_DSO_PATH.append('@/plugin')
        env.HOUDINI_DSO_PATH.append('&')
        env.HOUDINI_SCRIPT_PATH.append('@/scripts')
        env.HOUDINI_SCRIPT_PATH.append('{root}/lib/python')
        env.HOUDINI_SCRIPT_PATH.append('&')
        env.PYTHONPATH.append('{root}/lib/python')
    elif "renderman" in resolve:
        env.PYTHONPATH.append('{root}/lib/python')
        env.RMAN_SHADERPATH.append('{root}/plugin/usd/resources/shaders')
        env.RMAN_TEXTUREPATH.append('{root}/plugin/usd')
    else:
        env.PYTHONPATH.append("{base}/platform-linux/USD-Core/lib/python")
    env.PATH.prepend("{base}/platform-linux/USD-Core/bin")

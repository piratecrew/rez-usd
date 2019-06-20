# -*- coding: utf-8 -*-

name = 'usd'

version = '19.07'

authors = ['frbr']

build_requires = [
    "python-2.7-native",
    "virtualenv",
    "cmake-3+",
    "devtoolset-7",
]

variants = [
    ["platform-linux"],
    ["platform-linux", "houdini-17.0"],
    ["platform-linux", "houdini-17.5"],
    ["platform-linux", "maya-2018"],
    ["platform-linux", "maya-2019"]
]

build_command = "bash $REZ_BUILD_SOURCE_PATH/build_usd.sh"

def commands():
    env.PATH.prepend("{base}/.venv/bin")
    env.PYTHONPATH.append("{base}/USD-Core/lib/python")
    env.PATH.prepend("{base}/USD-Core/bin")
  
    if "maya" in resolve:
        env.MAYA_PLUG_IN_PATH.append('{root}/third_party/maya/plugin')
        env.MAYA_SCRIPT_PATH.append('{root}/third_party/maya/lib/usd/usdMaya/resources')
        env.MAYA_SCRIPT_PATH.append('{root}/third_party/maya/plugin/pxrUsdPreviewSurface/resources')
        env.PYTHONPATH.append('{root}/lib/python')
        env.XBMLANGPATH.append('{root}/third_party/maya/lib/usd/usdMaya/resources')
   
    if "houdini" in resolve:
        env.HOUDINI_PATH.append('{root}/third_party/houdini')
        env.HOUDINI_DSO_ERROR = 1
        env.HOUDINI_DSO_PATH.append('@/plugin')
        env.HOUDINI_DSO_PATH.append('&')
        env.HOUDINI_SCRIPT_PATH.append('@/scripts')
        env.HOUDINI_SCRIPT_PATH.append('{root}/lib')
        env.HOUDINI_SCRIPT_PATH.append('&')
        

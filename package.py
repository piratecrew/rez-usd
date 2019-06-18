# -*- coding: utf-8 -*-

name = 'usd'

version = '19.07'

authors = ['frbr']

variants = [["platform-linux"]]

build_command = """
if [[ $REZ_BUILD_INSTALL -eq 1 ]];
then
    mkdir -p $REZ_BUILD_INSTALL_PATH;
    # Create Virtualenv
    virtualenv --python=python2 $REZ_BUILD_INSTALL_PATH/.venv
    source $REZ_BUILD_INSTALL_PATH/.venv/bin/activate
    pip install PyOpenGL PySide2
    # Clone USD
    git clone https://github.com/PixarAnimationStudios/USD.git USD
    cd USD
    git checkout v$REZ_BUILD_PROJECT_VERSION
    # Build USD
    python build_scripts/build_usd.py $REZ_BUILD_INSTALL_PATH\
        --src $REZ_BUILD_SOURCE_PATH/build/DEP_SOURCE\
        --build $REZ_BUILD_SOURCE_PATH/build/DEP_BUILD\
        --inst $REZ_BUILD_INSTALL_PATH/dependencies\
        --openimageio --opencolorio --ptex\
        --alembic --no-hdf5\
        --materialx\
        --build-args OpenImageIO,-DOpenGL_GL_PREFERENCE=GLVND OpenColorIO,"-DCMAKE_CXX_FLAGS=-w"
  else
    echo not running rez-install;
fi
"""

def commands():
    env.PATH.prepend("{root}/.venv/bin")
    env.PYTHONPATH.append("{root}/lib/python")
    env.PATH.prepend("{root}/bin")

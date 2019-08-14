#!/bin/bash
set -e

# Find the actual install path
echo $REZ_BUILD_INSTALL_PATH
if [[ "$REZ_BUILD_INSTALL_PATH" =~ .*platform-linux$ ]]; then
    INSTALL_ROOT=$REZ_BUILD_INSTALL_PATH
else
    INSTALL_ROOT=$(dirname $REZ_BUILD_INSTALL_PATH)
fi

PROJECT_PATH=$REZ_BUILD_SOURCE_PATH
BUILD_ROOT=$REZ_BUILD_SOURCE_PATH/build
DEPENDENCIES_ROOT=$INSTALL_ROOT/USD-Dependencies
USD_CORE_ROOT=$INSTALL_ROOT/USD-Core

CORE_BUILD_FILE=$BUILD_ROOT/.core_built
echo "###### VARIABLE #######"
echo ""
echo "INSTALL_ROOT=$INSTALL_ROOT"
echo "PROJECT_PATH=$PROJECT_PATH"
echo "BUILD_ROOT=$BUILD_ROOT"
echo "DEPENDENCIES_ROOT=$DEPENDENCIES_ROOT"
echo "USD_CORE_ROOT=$USD_CORE_ROOT"
echo "CORE_BUILD_FILE=$CORE_BUILD_FILE"
echo ""
echo "#######################"

if [[ ! $REZ_BUILD_INSTALL -eq 1 ]];
then
    echo not running rez-install;
    exit 1
fi
mkdir -p $REZ_BUILD_INSTALL_PATH;

# Build USD-Core if needed
if [[ ! -f "$CORE_BUILD_FILE" ]]; then
    #As we are in a undefined variants environment
    # we need to clean it up when building USD-Core.
    # We store some ENV_VARS and restoring them later
    #OLD_PYTHONPATH=$PYTHONPATH
    #OLD_LD_LIBRARY_PATH=$LD_LIBRARY_PATH
    # Clear LD_LIBRARY_PATH to make sure we don't pickup variant specific libraries
    #unset LD_LIBRARY_PATH

    # Create Virtualenv
    #virtualenv --python=python2 $INSTALL_ROOT/.venv
    #source $INSTALL_ROOT/.venv/bin/activate
    #pip install PyOpenGL PySide2==5.12 Jinja2

    # Clone USD
    git clone https://github.com/PixarAnimationStudios/USD.git $BUILD_ROOT/USD || true
    cd $BUILD_ROOT/USD
    git checkout v$REZ_BUILD_PROJECT_VERSION

    ################################
    # Build USD-Core
    ################################

    # Houdini will mess up python path for PySide2.
    # We clear PYTHONPATH to use PySide2 from the virtualenv
    #unset PYTHONPATH

    python build_scripts/build_usd.py -v -v $USD_CORE_ROOT\
        --src $BUILD_ROOT/DEP_SOURCE\
        --build $BUILD_ROOT/DEP_BUILD\
        --inst $DEPENDENCIES_ROOT\
        --openimageio --opencolorio --ptex\
        --alembic --no-hdf5\
        --materialx\
        --build-args OpenImageIO,-DOpenGL_GL_PREFERENCE=GLVND OpenColorIO,"-DCMAKE_CXX_FLAGS=-w"
    # create build file to make sure we don't rebuild core for the other variants
    touch $CORE_BUILD_FILE
    # Deactivate the venv
    #echo "DEACTIVATE"
    #deactivate
    # Restore PYTHONPATH and LD_LIBRARY_PATH
    #export PYTHONPATH=$OLD_PYTHONPATH
    #export LD_LIBRARY_PATH=$OLD_LD_LIBRARY_PATH
else
    echo "USD Core already built, skipping"
    cd $BUILD_ROOT/USD
fi

# Now handle the current variant
# Is renderman variant?
if [[ ! -z "$REZ_RENDERMAN_ROOT" ]]; then
    export USD_VERSION=19.07
    export USD_ROOT=$USD_CORE_ROOT
    echo "Building Renderman variant: renderman-$REZ_RENDERMAN_MAJOR_VERSION.$REZ_RENDERMAN_MINOR_VERSION"
    rm $BUILD_ROOT/DEP_BUILD/USD/CMakeCache.txt || true
    python build_scripts/build_usd.py -v -v \
     $USD_CORE_ROOT\
     --src $BUILD_ROOT/DEP_SOURCE\
     --build $BUILD_ROOT/DEP_BUILD\
     --inst $DEPENDENCIES_ROOT\
     --prman --prman-location $REZ_RENDERMAN_ROOT --force prman \
     --build-args USD,-DCMAKE_INSTALL_PREFIX=$REZ_BUILD_INSTALL_PATH
fi 

# Now handle the current variant
# Is maya variant?
if [[ ! -z "$REZ_MAYA_ROOT" ]]; then
    export USD_VERSION=19.07
    export USD_ROOT=$USD_CORE_ROOT
    echo "Building Maya variant: maya-$REZ_MAYA_MAJOR_VERSION.$REZ_MAYA_MINOR_VERSION"
    rm $BUILD_ROOT/DEP_BUILD/USD/CMakeCache.txt || true
    python build_scripts/build_usd.py -v -v \
     $USD_CORE_ROOT\
     --src $BUILD_ROOT/DEP_SOURCE\
     --build $BUILD_ROOT/DEP_BUILD\
     --inst $DEPENDENCIES_ROOT\
     --maya --maya-location $REZ_MAYA_ROOT/maya --force maya \
     --build-args USD,-DCMAKE_INSTALL_PREFIX=$REZ_BUILD_INSTALL_PATH
fi
exit 0

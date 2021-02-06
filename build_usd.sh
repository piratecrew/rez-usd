#!/bin/bash
set -e

PROJECT_PATH=$REZ_BUILD_SOURCE_PATH
BUILD_ROOT=$PROJECT_PATH/build
DEPENDENCIES_ROOT=$(echo $REZ_BUILD_INSTALL_PATH | sed "s@$REZ_BUILD_VARIANT_SUBPATH@USD-Dependencies/$REZ_PLATFORM_VERSION/python-$REZ_PYTHON_MAJOR_VERSION.$REZ_PYTHON_MINOR_VERSION@g")

echo "###### VARIABLE #######"
echo ""
echo "REZ_BUILD_INSTALL_PATH=$REZ_BUILD_INSTALL_PATH"
echo "PROJECT_PATH=$PROJECT_PATH"
echo "BUILD_ROOT=$BUILD_ROOT"
echo "DEPENDENCIES_ROOT=$DEPENDENCIES_ROOT"
echo ""
echo "#######################"

if [[ ! $REZ_BUILD_INSTALL -eq 1 ]];
then
    echo not running rez-install;
    exit 1
fi

if [[ $REZ_IN_REZ_RELEASE -eq 1 ]];
then
    echo "Remove build files as we are releasing: $BUILD_ROOT/{DEP_BUILD,USD}";
    rm -rf $BUILD_ROOT/{DEP_BUILD,USD} || true
fi

mkdir -p $REZ_BUILD_INSTALL_PATH;

# Clone USD
git clone https://github.com/PixarAnimationStudios/USD.git $BUILD_ROOT/USD || true
cd $BUILD_ROOT/USD
git pull origin release
git checkout v$REZ_BUILD_PROJECT_VERSION

#python build_scripts/build_usd.py -h
#exit 0

################################
# Build USD
################################

if [[ $REZ_USED_RESOLVE == *"PySide2"* ]]; then
    python build_scripts/build_usd.py -v -v $REZ_BUILD_INSTALL_PATH\
    --src $BUILD_ROOT/DEP_SOURCE\
    --build $BUILD_ROOT/python-$REZ_PYTHON_MAJOR_VERSION.$REZ_PYTHON_MINOR_VERSION/DEP_BUILD\
    --inst $DEPENDENCIES_ROOT\
    --docs\
    --openimageio --opencolorio --ptex\
    --alembic --no-hdf5\
    --materialx\
    --build-args OpenImageIO,-DOpenGL_GL_PREFERENCE=GLVND OpenColorIO,"-DCMAKE_CXX_FLAGS=-w" USD, -DRPATH_INSTALL_PATH="\$ORIGIN/.;\$ORIGIN/../../..;$DEPENDENCIES_ROOT"
else
    python build_scripts/build_usd.py -v -v $REZ_BUILD_INSTALL_PATH\
    --src $BUILD_ROOT/DEP_SOURCE\
    --build $BUILD_ROOT/python-$REZ_PYTHON_MAJOR_VERSION.$REZ_PYTHON_MINOR_VERSION/DEP_BUILD\
    --inst $DEPENDENCIES_ROOT\
    --openimageio --opencolorio --ptex --no-usdview\
    --docs\
    --alembic --no-hdf5\
    --materialx\
    --build-args OpenImageIO,-DOpenGL_GL_PREFERENCE=GLVND OpenColorIO,-DCMAKE_CXX_FLAGS=-w" USD, "-DRPATH_INSTALL_PATH="\$ORIGIN/.;\$ORIGIN/../../..;$DEPENDENCIES_ROOT"
fi

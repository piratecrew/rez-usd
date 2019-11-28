#!/bin/bash
set -e

PROJECT_PATH=$REZ_BUILD_SOURCE_PATH
BUILD_ROOT=$REZ_BUILD_SOURCE_PATH/build
USD_CORE_ROOT=$INSTALL_ROOT/USD-Core
DEPENDENCIES_ROOT=$(echo $REZ_BUILD_INSTALL_PATH | sed "s@$REZ_BUILD_VARIANT_SUBPATH@USD-Dependencies/$REZ_PLATFORM_VERSION@g")

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
mkdir -p $REZ_BUILD_INSTALL_PATH;

# Clone USD
git clone https://github.com/PixarAnimationStudios/USD.git $BUILD_ROOT/USD || true
cd $BUILD_ROOT/USD
git checkout v$REZ_BUILD_PROJECT_VERSION

#python build_scripts/build_usd.py -h
#exit 0

################################
# Build USD
################################

if [[ $REZ_USED_RESOLVE == *"PySide"* ]]; then
    python build_scripts/build_usd.py -v -v $REZ_BUILD_INSTALL_PATH\
    --src $BUILD_ROOT/DEP_SOURCE\
    --build $BUILD_ROOT/DEP_BUILD\
    --inst $DEPENDENCIES_ROOT\
    --openimageio --opencolorio --ptex --force boost\
    --alembic --no-hdf5\
    --materialx\
    --build-args OpenImageIO,-DOpenGL_GL_PREFERENCE=GLVND OpenColorIO,"-DCMAKE_CXX_FLAGS=-w"
else
    python build_scripts/build_usd.py -v -v $REZ_BUILD_INSTALL_PATH\
    --src $BUILD_ROOT/DEP_SOURCE\
    --build $BUILD_ROOT/DEP_BUILD\
    --inst $DEPENDENCIES_ROOT\
    --no-imaging\
    --alembic --no-hdf5\
    --materialx\
    --build-args OpenImageIO,-DOpenGL_GL_PREFERENCE=GLVND OpenColorIO,"-DCMAKE_CXX_FLAGS=-w"
fi

CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

include(RezBuild)
include(ExternalProject)

rez_find_packages(PREFIX pkgs AUTO)

set(usd_version ${USD_VERSION})
set(url_usd https://github.com/PixarAnimationStudios/USD/archive/v${usd_version}.zip)

if(${REZ_BUILD_INSTALL})
    set(install_cmd make install ${make_args})
else()
    set(install_cmd "")
endif()

message(STATUS "-DPTEX_LOCATION=$ENV{REZ_PTEX_ROOT}")

set(CMAKE_ARGS
	-DBUILD_SHARED_LIBS=ON
	-DPXR_BUILD_MONOLITHIC=OFF
	-DPXR_BUILD_IMAGING=ON
    # TBB
    -DTBB_INCLUDE_DIR=${tbb_INCLUDE_DIRS}
    -DTBB_LIBRARY=${tbb_LIBRARY_DIRS}
    # OPENEXR
    -DOPENEXR_INCLUDE_DIR=${openexr_INCLUDE_DIRS}
    -DOPENEXR_LIBRARY_DIR=${openexr_LIBRARY_DIRS}
    # PTEX
	-DPXR_ENABLE_PTEX_SUPPORT=ON
    -DPTEX_LOCATION=$ENV{REZ_PTEX_ROOT}
    # OIIO
    -DOIIO_INCLUDE_DIR=${oiio_INCLUDE_DIRS}
    -DOIIO_LIBRARIES=${oiio_LIBRARIES}
    # GLEW
    -DGLEW_INCLUDE_DIR=${glew_INCLUDE_DIRS}
    -DGLEW_LIBRARY=${glew_LIBRARIES}
    # OEPNSUBDIV
    -DOPENSUBDIV_ROOT_DIR=$ENV{REZ_OPENSUBDIV_ROOT}
)

ExternalProject_add(
    usd
    URL ${url_usd}
    PREFIX usd
    CMAKE_ARGS -DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX} ${CMAKE_ARGS}
    INSTALL_COMMAND "${install_cmd}"
)

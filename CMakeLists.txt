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

message(STATUS "-DTBB_INCLUDE_DIR=${tbb_INCLUDE_DIRS}")
message(STATUS "-DTBB_LIBRARY=${tbb_LIBRARY_DIRS}")

set(CMAKE_ARGS
	-DBUILD_SHARED_LIBS=ON
	-DPXR_BUILD_MONOLITHIC=ON
	-DPXR_BUILD_IMAGING=ON
	-DPXR_ENABLE_PTEX_SUPPORT=OFF
	#-DTBB_ROOT_DIR=${REZ_TBB_ROOT}
	-DTBB_INCLUDE_DIR=${tbb_INCLUDE_DIRS}
	-DTBB_LIBRARY=${tbb_LIBRARY_DIRS}
	-DOPENEXR_LOCATION=$ENV{REZ_OPENEXR_ROOT}
	-DOIIO_LOCATION=$ENV{REZ_OIIO_ROOT}
	-DGLEW_LOCATION=$ENV{REZ_GLEW_ROOT}
	-DOPENSUBDIV_ROOT_DIR=${REZ_OPENSUBDIV_ROOT}
	-DPXR_BUILD_MAYA_PLUGIN=ON
	-DMAYA_LOCATION=$ENV{REZ_MAYA_ROOT}/ext
)

ExternalProject_add(
    usd
    URL ${url_usd}
    PREFIX usd
    CMAKE_ARGS -DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX} ${CMAKE_ARGS}
    INSTALL_COMMAND "${install_cmd}"
)

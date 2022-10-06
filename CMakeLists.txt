SET(PROJECT_NAME Subsense)
PROJECT(${PROJECT_NAME})
CMAKE_MINIMUM_REQUIRED (VERSION 2.8.3)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Set a default build type if none was specified
set(default_build_type "Release")
if(NOT CMAKE_BUILD_TYPE AND NOT WIN32)
  message(STATUS "Setting build type to '${default_build_type}' as none was specified.")
  set(CMAKE_BUILD_TYPE "${default_build_type}" CACHE
      STRING "Choose the type of build." FORCE)
  # Set the possible values of build type for cmake-gui
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release"
    "MinSizeRel" "RelWithDebInfo")
endif()

SET(GCC_FASTMATH_FLAGS "-ffast-math -funsafe-math-optimizations -msse4.2")
SET(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} ${GCC_FASTMATH_FLAGS}")

find_package (OpenCV REQUIRED)
message(STATUS "OpenCV_INCLUDE_DIRS => ${OpenCV_INCLUDE_DIRS}")
message(STATUS "OpenCV_LIBS : ${OpenCV_LIBS}")
include_directories(${OpenCV_INCLUDE_DIRS})

set(SS_DIR ${CMAKE_CURRENT_SOURCE_DIR})

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Ofast")

 if(APPLE)
    set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
    set(CMAKE_INSTALL_NAME_DIR ${CMAKE_INSTALL_PREFIX}/lib)
    set(CMAKE_MACOSX_RPATH ON)
    set(CMAKE_SKIP_BUILD_RPATH FALSE)
    set(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE)
    set(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")
    set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
endif()

file(GLOB LIB_SRC_FILES ${SS_DIR}/Subsense/*.cpp)
include_directories(${SS_DIR})

add_library(Subsense SHARED ${LIB_SRC_FILES})
target_link_libraries(Subsense ${OpenCV_LIBS})

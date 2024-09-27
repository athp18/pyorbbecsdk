# CMakeLists.txt

cmake_minimum_required(VERSION 3.15)
project(pyorbbecsdk LANGUAGES C CXX)

# Set C++ and C standards
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_C_STANDARD 11)

# Set compiler flags
if(MSVC)
    add_compile_options(/W4)
else()
    add_compile_options(-Wall -Wextra -Wpedantic -fPIC -O3)
endif()

# cmake mods
include(${CMAKE_CURRENT_SOURCE_DIR}/cmake/DetermineHostPlatform.cmake)

# find python
find_package(Python3 COMPONENTS Interpreter Development.Module REQUIRED)
find_package(pybind11 CONFIG REQUIRED)

# Find Orbbec SDK headers and libraries
find_path(ORBBEC_INCLUDE_DIR NAMES OrbbecSDK.h PATHS ${CMAKE_CURRENT_SOURCE_DIR}/sdk/include)

if (WIN32)
    set(ORBBEC_LIB_PREFIX "")
    set(ORBBEC_LIB_SUFFIX ".lib")
elseif(APPLE)
    set(ORBBEC_LIB_PREFIX "lib")
    set(ORBBEC_LIB_SUFFIX ".dylib")
elseif (UNIX)
    set(ORBBEC_LIB_PREFIX "lib")
    set(ORBBEC_LIB_SUFFIX ".so")
endif()

set(HOST_PLATFORM ${CMAKE_SYSTEM_NAME})
set(ORBBEC_LIBS_DIR ${CMAKE_CURRENT_SOURCE_DIR}/sdk/lib/${HOST_PLATFORM})

find_library(ORBBECSDK_LIB
    NAMES ${ORBBEC_LIB_PREFIX}OrbbecSDK${ORBBEC_LIB_SUFFIX}
    PATHS ${ORBBEC_LIBS_DIR}
    NO_DEFAULT_PATH
)

if(NOT ORBBEC_INCLUDE_DIR OR NOT ORBBECSDK_LIB)
    message(FATAL_ERROR "Orbbec SDK not found. Please ensure it's included in the package or installed on your system.")
endif()

# Include directories
include_directories(
    ${ORBBEC_INCLUDE_DIR}
    src/pyorbbecsdk/
)

# Add the pybind11 module
pybind11_add_module(${PROJECT_NAME}
    src/pyorbbecsdk/pyorbbecsdk.cpp
    src/pyorbbecsdk/context.cpp
    src/pyorbbecsdk/device.cpp
    src/pyorbbecsdk/error.cpp
    src/pyorbbecsdk/filter.cpp
    src/pyorbbecsdk/frame.cpp
    src/pyorbbecsdk/pipeline.cpp
    src/pyorbbecsdk/properties.cpp
    src/pyorbbecsdk/record_playback.cpp
    src/pyorbbecsdk/sensor.cpp
    src/pyorbbecsdk/stream_profile.cpp
    src/pyorbbecsdk/types.cpp
    src/pyorbbecsdk/utils.cpp
)

# Link the Orbbec SDK library
target_link_libraries(${PROJECT_NAME} PRIVATE ${ORBBECSDK_LIB})

# Install the module
install(TARGETS ${PROJECT_NAME}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_LIBDIR}
)

# include tests option
option(BUILD_TESTING "Build tests" ON)
if(BUILD_TESTING)
    enable_testing()

    set(PY_TEST_SRCS
        test/test_context.py
        test/test_device.py
        test/test_pipeline.py
        test/test_sensor_control.py
    )

    foreach(PY_TEST_SRC ${PY_TEST_SRCS})
        get_filename_component(PY_TEST_NAME ${PY_TEST_SRC} NAME_WE)
        add_test(NAME ${PY_TEST_NAME}
            COMMAND ${Python3_EXECUTABLE} -v ${CMAKE_CURRENT_SOURCE_DIR}/${PY_TEST_SRC}
        )
    endforeach()
endif()

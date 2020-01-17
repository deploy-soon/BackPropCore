cmake_minimum_required (VERSION 2.8.8)
project (cbackpropcore)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14 -fPIC -Wall -Wextra -fopenmp -O3 -ggdb -march=native")
set(CMAKE_VERBOSE_MAKEFILE true)

include (GNUInstallDirs)

include_directories("./include")
include_directories("./3rd/spdlog/include")
include_directories("./3rd/eigen3")

file(GLOB MISC_SRCS ${CMAKE_CURRENT_SOURCE_DIR}/lib/misc/*.cc)
add_library(cbackpropcore SHARED ${SOURCES} ${MISC_SRCS})
include_directories(cbackpropcore "/usr/local/include/eigen3")

set_target_properties(cbackpropcore PROPERTIES VERSION 0.1)

install(TARGETS cbackpropcore
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR})

install(DIRECTORY "${CMAKE_SOURCE_DIR}/include/backpropcore"
    DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}"
    FILES_MATCHING
    PATTERN "*.hpp"
)

cmake_minimum_required(VERSION 3.16)
project(cpp)

set(CMAKE_CXX_STANDARD 14)

find_package(Boost 1.72.0 COMPONENTS system filesystem REQUIRED)
include_directories(${Boost_INCLUDE_DIRS})

add_executable(cpp src/main.cpp src/lexer/NFA.cpp src/lexer/NFA.h src/lexer/State.h src/lexer/DFA.cpp src/lexer/DFA.h src/lexer/Utils.h)
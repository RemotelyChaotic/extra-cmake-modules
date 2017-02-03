cmake_minimum_required(VERSION 2.8.12 FATAL_ERROR)

get_filename_component(PYTHON_UMBRELLA_MODULE_DIR ${PYTHON_UMBRELLA_MODULE_FILE} PATH)

file(MAKE_DIRECTORY "${PYTHON_UMBRELLA_MODULE_DIR}")

execute_process(COMMAND "${CMAKE_COMMAND}" -E touch "${PYTHON_UMBRELLA_MODULE_FILE}")
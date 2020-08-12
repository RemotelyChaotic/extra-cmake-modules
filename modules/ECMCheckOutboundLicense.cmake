#.rst:
# ECMCheckOutboundLicense
# -----------
#
# Convenience functions for license test
#
# ::
#
#   ecm_check_outbound_license(LICENSE <outbound-license>
#                              FILES <source-files>
#                              TEST_NAME <name>)
#
# This method adds a custom unit test to ensure the specified outbound license to be
# compatible with the specified license headers.
#
#
# Since 5.74.0

function(ecm_check_outbound_license)
    set(_oneValueArgs LICENSE TEST_NAME)
    set(_multiValueArgs FILES)
    cmake_parse_arguments(ARG "" "${_oneValueArgs}" "${_multiValueArgs}" ${ARGN} )

    if(NOT ARG_LICENSE)
        message(FATAL_ERROR "No LICENSE argument given to ecm_check_outbound_license")
    endif()

    if(NOT ARG_FILES)
        message(FATAL_ERROR "No FILES argument given to ecm_check_outbound_license")
    endif()

    # generate file with list of relative file paths
    string(REPLACE "${CMAKE_BINARY_DIR}/" "" RELATIVE_PREFIX_PATH ${CMAKE_CURRENT_BINARY_DIR})
    set(OUTPUT_FILE ${CMAKE_BINARY_DIR}/licensecheck_${ARG_TEST_NAME}.txt)
    message("Generate test input file: ${OUTPUT_FILE}")
    file(REMOVE ${OUTPUT_FILE})
    foreach(_file ${ARG_FILES})
        # check script expects files to start with "./", which must be relative to CMAKE_SOURCE_DIR
        if (IS_ABSOLUTE ${_file})
            string(REPLACE ${CMAKE_SOURCE_DIR} "." TEMPORARY_PATH ${_file})
            file(APPEND ${OUTPUT_FILE} "${TEMPORARY_PATH}\n")
        else()
            file(APPEND ${OUTPUT_FILE} "./${RELATIVE_PREFIX_PATH}/${_file}\n")
        endif()
    endforeach()

    file(COPY ${CMAKE_SOURCE_DIR}/modules/check-outbound-license.py DESTINATION ${CMAKE_BINARY_DIR})

    # TODO test only run when running CMake, make it an implicit call when running tests
    if (NOT DEFINED SPDX_TOOL_EXECUTED)
        message("Executing reuse tool...")
        execute_process(COMMAND bash -c "reuse spdx" WORKING_DIRECTORY ${CMAKE_SOURCE_DIR} OUTPUT_FILE ${CMAKE_BINARY_DIR}/spdx.txt)
        set(SPDX_TOOL_EXECUTED TRUE PARENT_SCOPE)
    endif()

    add_test(NAME licensecheck_${ARG_TEST_NAME} COMMAND python3 ${CMAKE_BINARY_DIR}/check-outbound-license.py -l ${ARG_LICENSE} -s ${CMAKE_BINARY_DIR}/spdx.txt -i ${OUTPUT_FILE})
endfunction()

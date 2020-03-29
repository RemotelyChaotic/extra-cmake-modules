set(MODULES_DIR "${ECM_SOURCE_DIR}/modules")

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/../../modules)
include(ECMCheckOutboundLicense)

ecm_check_outbound_license(
LICENSE LGPL-2.1-only
TEST_NAME valid-LGPL-2.1-only
FILES
    testcase_valid_LGPL-2.1/BSD-2-Clause.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/testcase_valid_LGPL-2.1/LGPL-2.1-or-later.cpp
)

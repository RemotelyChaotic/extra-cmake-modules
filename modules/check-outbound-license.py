#!/usr/bin/env python3

# key is the target out-bound license
# value list are licenses that are compatible with the target license
compatibilityMatrix = {
    "LGPL-2.0-only": [
        "LGPL-2.0-only",
        "LGPL-2.0-or-later",
        "MIT",
        "BSD-2-Clause",
        "BSD-3-Clause"],
    "LGPL-2.1-only": [
        "LGPL-2.0-or-later",
        "LGPL-2.1-only",
        "LGPL-2.1-or-later",
        "MIT",
        "BSD-2-Clause",
        "BSD-3-Clause"],
    "LGPL-3.0-only": [
        "LGPL-2.0-or-later",
        "LGPL-2.1-or-later",
        "LGPL-3.0-only",
        "LGPL-3.0-or-later",
        "MIT",
        "BSD-2-Clause",
        "BSD-3-Clause"],
    "GPL-2.0-only": [
        "LGPL-2.0-only",
        "LGPL-2.1-only",
        "LGPL-2.0-or-later",
        "LGPL-2.1-or-later",
        "GPL-2.0-only",
        "GPL-2.0-or-later",
        "MIT",
        "BSD-2-Clause",
        "BSD-3-Clause"],
    "GPL-3.0-only": [
        "LGPL-2.0-or-later",
        "LGPL-2.1-or-later",
        "LGPL-3.0-only",
        "LGPL-3.0-or-later",
        "GPL-2.0-or-later",
        "GPL-3.0-only",
        "GPL-3.0-or-later",
        "MIT",
        "BSD-2-Clause",
        "BSD-3-Clause"]
}

# check that all files have compatible licenses with the taret license
# license paramter shall be base license name (e.g. "LGPL-2.1" or "MIT")
def check_outbound_license(license, files, spdxDictionary):
    print("Checking Target License: " + license)
    if not license in compatibilityMatrix:
        print("Error: unknown license selected")
        return False

    missingCompatibleLicense = False

    for sourceFile in files:
        compatible = False
        sourceFileStripped = sourceFile.strip()
        for fileLicense in spdxDictionary[sourceFileStripped]:
            if fileLicense in compatibilityMatrix[license]:
                compatible = True
                print("OK " + sourceFileStripped + " : " + fileLicense)
        if compatible == False:
            missingCompatibleLicense = True
            print("-- " + sourceFileStripped + " : ( " + ", ".join([str(i) for i in spdxDictionary[sourceFileStripped]]) + " )")
    return missingCompatibleLicense == False

if __name__ == '__main__':
    print("Parsing SPDX BOM file")
    import sys
    import argparse

    # parse commands
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--license", help="set outbound license to test")
    parser.add_argument("-s", "--spdx", help="spdx bill-of-materials file")
    parser.add_argument("-i", "--input", help="input file with list of source files to test")
    args = parser.parse_args()

    # TODO check if required arguments are present and give meaningful feedback

    # collect name and licenses from SPDX blocks
    spdxDictionary = {}
    fileName = ""
    licenses = []
    f = open(args.spdx, "r")
    for line in f:
        if line.startswith("FileName:"):
            # strip "FileName: "
            # thus name expected to start with "./", which is relative to CMAKE_SOURCE_DIR
            fileName = line[10:].strip()
        if line.startswith("LicenseInfoInFile:"):
            licenses.append(line[19:].strip())
        if line == '' or line == "\n":
            spdxDictionary[fileName] = licenses
            fileName = ""
            licenses = []
    f.close();

    # read file with list of test files
    f = open(args.input, "r")
    testfiles = f.readlines()
    f.close()

    if check_outbound_license(args.license, testfiles, spdxDictionary) == True:
        sys.exit(0);

    # in any other case, return error code
    sys.exit(1)
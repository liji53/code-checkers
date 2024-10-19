#!/usr/bin/env bash

testClangTidyReplacement() {
    local buildDirectory=${1-build}
    local updateExpected=${2-0}
    local filePath="${3}"
    local expectedFilePath="${4}"
    local checkName="${5}"
    local checkLib="${6}"

    GREEN='\033[0;32m'
    NO_COLOR='\033[0m'
    RED='\033[0;31m'

    cp "$filePath" "$filePath.bak"

    testPassed="true"
    clang-tidy-16 \
        --checks="-*,$checkName" \
        --fix \
        --load="$buildDirectory/lib/$checkLib" \
        -p "$buildDirectory/compile_commands.json" \
        "$filePath" || true
    clang-format-16 -i "$filePath"
    echo "The diff between '$filePath' and '$expectedFilePath' is:"
    diff --color "$filePath" "$expectedFilePath" -w \
        || testPassed="false"
    if [[ "$updateExpected" == "1" ]]; then
        echo "Updating '$filePath' file with the current replacements"
        cp "$filePath" "$expectedFilePath"
    fi

    mv "$filePath.bak" "$filePath"

    if [[ "$testPassed" == "true" ]]; then
        echo -e "${GREEN}PASSED${NO_COLOR}"
    else
        echo -e "${RED}FAILED${NO_COLOR}"
    fi
}
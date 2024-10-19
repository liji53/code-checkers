#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

buildDirectory=${1-build}

SCRIPT_DIRECTORY="$(dirname "$(readlink --canonicalize "$0")")"


"$SCRIPT_DIRECTORY/src/assign_mistake_by_equal/test.sh" "$buildDirectory"

"$SCRIPT_DIRECTORY/src/condition_mistake_by_assign/test.sh" "$buildDirectory"

"$SCRIPT_DIRECTORY/src/snprintf_arg_count/test.sh" "$buildDirectory"
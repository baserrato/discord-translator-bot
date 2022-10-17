#!/usr/bin/env bash

set -euo pipefail

function output {
  echo "::set-output name=${1}::${2}"
}

flags=(--ci)

previousVersion=$(git describe --tags --abbrev=0)
output "previousVersion" "${previousVersion}"

node_modules/semantic-release/bin/semantic-release.js "${flags[@]}"

newVersion=$(git describe --tags --abbrev=0)
output "newVersion" "${newVersion}"

changed="true"

if [ "$previousVersion" == "$newVersion" ]; then
  changed="false"
fi

output "changed" "${changed}"

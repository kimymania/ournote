#!/bin/bash
# Delete old client and regenerate
rm -rf ./lib/api_client
openapi-generator-cli generate -i http://127.0.0.1:8000/openapi.json -g dart -o ./lib/api_client
#!/bin/bash
find . -type f -iname "*.sh" -exec chmod +x {} \;
./config/setup/setup.sh

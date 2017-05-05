#!/bin/bash

cd .. 
find . -name '*.vm' -exec ./VMtranslator '{}' \;

exit()


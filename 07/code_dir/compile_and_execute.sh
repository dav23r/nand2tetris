#!/bin/bash

# Translate all vm files to asm 
find .. -name '*.vm' -exec ./VMtranslator '{}' \;


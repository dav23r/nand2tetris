#!/bin/bash

red="\033[0;31m"
green="\033[;32m"
usual="\033[0m"

# determines whether file is a directory and contains vm files
function needs_translation(){
    file_name=$1
    if [ ! -d $file_name ]; then
        exit -1;
    fi
    ls $file_name | grep -E '*.vm' &> /dev/null
    exit $?
}

function translate(){
    dir_name=$1
    printf "Translating files in directory ${dir_name}\n"
    ./VMtranslator $dir_name
    exit $?
}

# export to subshells
export -f needs_translation 
export -f translate


# Find directories containing .vm files, run translator on them
# and generate .ams file in each

find .. -exec bash -c "needs_translation {}"    \;   \
            -a  \( -exec bash -c "translate {}" \;   \
                    -a -exec printf "Vm files in {} ${green}sucessfully${usual} translated\n\n"     \; \
                    -o -exec printf "${red}Error${usual} in translation of files located in {}\n\n" \; \
                \)

if [ $? -eq 0 ]; then
    echo -e ">> ${green}No errors reported :)${usual} <<"
else
    echo -e ">> ${red}Errors were reported during translation of one or more files :(${usual} <<"
fi



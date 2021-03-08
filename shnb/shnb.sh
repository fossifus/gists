#!/bin/bash

set -euo pipefail

# parameters
CONFIG_DIR="/Users/fossifus/.shnb"
STORAGE_DIR="${CONFIG_DIR}/notebooks"
DEFAULT_FILE="fossifus.ish"

# ls colors
COLOR="$(tput setaf 3)"
NO_COLOR="$(tput sgr0)"

# copy args to array
ARGS=( $@ )
NUM_ARGS=$#

# append file paths to arary
FILES=( "$STORAGE_DIR/$DEFAULT_FILE" )

# if "help" passed, list files
if [[ $NUM_ARGS > 0 && ( ${ARGS[0]} == h || ${ARGS[0]} == help || ${ARGS[0]} = "-h" || ${ARGS[0]} == "--help" ) ]]; then
    echo "shnb [file1...]: open default notebook and specified files"
    echo "shnb ls : list notebooks"
    echo "shnb rm file1 [file2...] : delete notebooks"
    exit 0
fi


# if "ls" passed, list files
if [[ $NUM_ARGS > 0 && ${ARGS[0]} == ls ]]; then
    ls -1 "$STORAGE_DIR" | grep '.ish' | sed 's/\.ish//g' | sed "s/^/$COLOR/g" | sed "s/$/$NO_COLOR/g" | column -x
    exit 0
fi

# if "rm" passed, rm files
if [[ $NUM_ARGS > 0 && ${ARGS[0]} == rm ]]; then
    # handle no filenames passed
    if [[ $NUM_ARGS == 1 ]]; then
        echo "Error: did not receive filenames to delete."
        exit 1
    fi
    # loop over filenames passed
    for i in $(seq 1 $(($NUM_ARGS - 1))); do
        # check file exists
        file="$(basename $STORAGE_DIR/${ARGS[i]} .ish)"
        if [[ ! -e "$STORAGE_DIR/$file.ish" ]]; then
            echo "File \"$STORAGE_DIR/${file}.ish\" doesn\'t exist, skipping..."
        else
            # prompt user for delete or skip
            while true; do
                read -p "Delete file $STORAGE_DIR/${file}.ish? [Yy/Nn] " yn
                case $yn in
                    [Yy]* ) rm "$STORAGE_DIR/${file}.ish"; break;;
                    [Nn]* ) exit;;
                    * ) echo "Please answer yes or no.";;
                esac
            done
        fi
    done
    exit 0
fi

# default: correct args and open files in ShellNotebook
if [[ $NUM_ARGS > 0 ]]; then
    for i in $(seq 0 $(($NUM_ARGS - 1))); do
        # check if filename is a path
        if [[ "${ARGS[i]}" != /* && "${ARGS[i]}" != ~/* ]]; then
            # if it's not a path then create file in ~/.shnb/
            ARGS[i]="${STORAGE_DIR}/${ARGS[i]}"
        fi
        # append extension if it doesn't have one
        if [[ "${ARGS[i]}" != *.ish ]]; then
            ARGS[i]="${ARGS[i]}.ish"
        fi
        # create file if doesn't exist
        if [[ ! -e "${ARGS[i]}" ]]; then
            # prompt user for create or bail
            while true; do
                read -p "File \""${ARGS[i]}"\" doesn\'t exist, create [Yy] or bail [Nn]? " yn
                case $yn in
                    [Yy]* ) cp "$CONFIG_DIR/template.ish" "${ARGS[i]}"; break;;
                    [Nn]* ) exit;;
                    * ) echo "Please answer yes or no.";;
                esac
            done
        fi
        # append corrected file name
        FILES+=( "${ARGS[i]}" )
    done
fi

# finally, open the files
open -a "Shell Notebook"
sleep 1.5
open ${FILES[@]}

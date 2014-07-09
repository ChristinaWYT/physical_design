#!/bin/bash

# loop & print a folder recusively,
print_folder_recurse() {
    for i in "$1"/*;do
        if [ -d "$i" ];then
            echo "dir: $i"
            print_folder_recurse "$i"
        elif [ -f "$i" ]; then
            echo "file: $i"
        fi
    done
}


# try get path from param
path=""
if [ -d "$1" ]; then
    path=$1;
else
    path="/tmp"
fi

echo "base path: $path"
print_folder_recurse $path

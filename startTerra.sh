#!/bin/bash

declare -a docFolder

nameDoc=$(echo $PWD | tr "/" "\n")

for folder in $nameDoc
do
    docFolder=(${docFolder[@]} "$folder")
done

#echo "${docFolder[2]}"

cd ~/${docFolder[2]}/SmartTerrariumR
exec ./SmartTerra.AppImage
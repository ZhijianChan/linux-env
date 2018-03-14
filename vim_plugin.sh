#!/bin/bash
if [ $1 = "install" ]; then
    vim +PluginInstall +qall
elif [ $1 = "update" ]; then
    vim +PluginUpdate +qall
fi

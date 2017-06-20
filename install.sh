#!/bin/zsh
root_dir=$PWD

# install oh-my-zsh
if [ ! -d ~/.oh-my-zsh ]; then
    rm -rf ~/.oh-my-zsh
    sh -c "$(wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"
else
    cd ~/.oh-my-zsh && git checkout .
fi

if [ ! -d ~/.bin ]; then
    mkdir ~/.bin
fi
if [ ! -d ~/.vim/colors ]; then
    mkdir ~/.vim/colors
fi

cd $root_dir
cp ./tmux.conf ~/.tmux.conf
cp ./zshrc ~/.zshrc
cp ./gitconfig ~/.gitconfig
cp ./vimrc ~/.vimrc
cp ./molokai.vim ~/.vim/colors/molokai.vim
cp ./atom ~/.bin/atom
cp ./clang-format ~/.clang-format

sh ~/.oh-my-zsh/tools/upgrade.sh
cp ./pwzer.zsh-theme ~/.oh-my-zsh/themes/

source ~/.zshrc

# vim
#git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
#git clone https://github.com/Valloric/YouCompleteMe.git ~/.vim/bundle/YouCompleteMe
#cd ~/.vim/bundle/YouCompleteMe
#git submodule update --init --recursive
#./install.py --clang-completer

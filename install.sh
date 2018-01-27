#!/bin/zsh
root_dir=$PWD

cp ./tmux.conf ~/.tmux.conf
cp ./zshrc ~/.zshrc
cp ./gitconfig ~/.gitconfig
cp ./vimrc ~/.vimrc
cp ./clang-format ~/.clang-format

# install oh-my-zsh
if [ ! -d ~/.oh-my-zsh ]; then
    rm -rf ~/.oh-my-zsh
    sh -c "$(wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"
else
    cd ~/.oh-my-zsh && git checkout .
fi
cd $root_dir
$(cp ./pwzer.zsh-theme ~/.oh-my-zsh/themes/)

if [ ! -d ~/.bin ]; then
    mkdir ~/.bin
fi

if [ ! -d ~/.config ]; then
    mkdir ~/.config
fi
cp ./flake8 ~/.config/flake8

if [ ! -d ~/.vim/colors ]; then
    mkdir -p ~/.vim/colors
fi
cp ./molokai.vim ~/.vim/colors/molokai.vim
cp ./solarized.vim ~/.vim/colors/solarized.vim

if [ ! -d ~/.supervisord ]; then
    sudo pip install supervisor
    mkdir -p ~/.supervisord/log
    mkdir -p ~/.supervisord/conf.d
    mkdir -p ~/.supervisord/tmp
fi
cp ./supervisord.conf ~/.supervisord/supervisord.conf

sh ~/.oh-my-zsh/tools/upgrade.sh
source ~/.zshrc

# vim
#git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
#git clone https://github.com/Valloric/YouCompleteMe.git ~/.vim/bundle/YouCompleteMe
#cd ~/.vim/bundle/YouCompleteMe
#git submodule update --init --recursive
#./install.py --clang-completer

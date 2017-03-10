#!/bin/zsh

# install oh-my-zsh
rm -rf ~/.oh-my-zsh
sh -c "$(wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"

cp ./tmux.conf ~/.tmux.conf
cp -rf ./oh-my-zsh ~/.oh-my-zsh
cp ./zshrc ~/.zshrc
cp ./gitconfig ~/.gitconfig
cp ./vimrc ~/.vimrc

sh ~/.oh-my-zsh/tools/upgrade.sh
cp ./pwzer.zsh-theme ~/.oh-my-zsh/themes/

source ~/.zshrc

# vim
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
git clone https://github.com/Valloric/YouCompleteMe.git ~/.vim/bundle/YouCompleteMe
cd ~/.vim/bundle/YouCompleteMe
git submodule update --init --recursive
./install.py --clang-completer

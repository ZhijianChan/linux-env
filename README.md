### **iTerm2**
这些配置都是在Mac本地主机执行的

- 主题配置
    `iTerm2` 这里使用的是 [solarized](http://ethanschoonover.com/solarized) 主题，github项目主页 [https://github.com/altercation/solarized](https://github.com/altercation/solarized)。
    
    ```zsh
    git clone https://github.com/altercation/solarized.git
    ```
    `iTerm2` -> `Preferences` -> `Profiles` -> `Colors` -> `Color Presets` -> `import`，选择 `solarized/iterm2-colors-solarized/Solarized Dark.itermcolors` 文件。

    为了配置 `dir_colors` 需要装 `coreutils`。

    ```zsh
    brew install coreutils gnu-getopt

    # 校验是否已经安装
    brew list | grep coreutils gnu-getopt
    brew --prefix coreutils gnu-getopt
    ```
- 字体配置

    为了显示主题中的特殊字符，需要安装 [Powerline](https://powerline.readthedocs.io/en/master/) 字体。

    ```zsh
    pip install --user powerline-status
    ```
    然后重启 `iTerm2`。`iTerm2` -> `Preferences` -> `Profiles` -> `Colors` -> `Test` -> `Change Font`。使用带`powerline`关键字的字体都可以。

### **服务器**
- clone 最新代码

    ```
    git clone git@git.tuputech.com:duguiping/ZSHENV.git ~/.zshenv
    ```

- 安装 `oh-my-zsh`、`tmux`、`zsh` 等基本环境

    ```zsh
    cd ~/.zshenv
    python install.py --name=<xxx> --email=<xxx@tuputech.com>
    ```

- 安装或更新 `vim` 插件

    ```zsh
    # install
    ./vim_plugin.sh install
    
    # update
    ./vim_plugin.sh update
    ```

- 使配置生效

    ```zsh
    source ~/.zshrc
    ```

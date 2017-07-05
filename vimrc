set background=dark
colorscheme molokai 
"colorscheme solarized
set term=xterm-256color
"set term=xterm
"set term=screen
"set t_Co=256
"语法高亮
set mouse=a
set ignorecase
syntax enable
syntax on
set laststatus=2
set scrolloff=3
set ruler
"Tab宽度
set ts=4
set expandtab
"自动缩进
set cindent
"缩进宽度
set shiftwidth=4
"关闭错误信息响铃
set noerrorbells
"显示行号
set number
"set hlsearch
set cursorcolumn
set cursorline
" 设置折叠
set foldmethod=manual

set guifont=YaHei\Consolas\Hybrid\11.5

" 关闭文件时保存视图，打开文件时自动导入视图，配合代码折叠使用
set viewdir=$HOME/.vim/view 
"autocmd BufWrite,FileWritePost * mkview
"autocmd BufRead,FileReadPost * loadview

"required
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
"VIM插件管理工具
Plugin 'VundleVim/Vundle.vim'
"代码补全
Plugin 'jiangmiao/auto-pairs'
Plugin 'tpope/vim-fugitive'
Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}
Plugin 'ascenator/L9', {'name': 'newL9'}
"Plugin 'scrooloose/syntastic'
"目录树
Plugin 'scrooloose/nerdtree'
"search file
Plugin 'kien/ctrlp.vim'
"python-doc
"Plugin 'python-mode/python-mode'
Plugin 'Valloric/YouCompleteMe'
"对齐工具 
Plugin 'godlygeek/tabular'
"快速注释
Plugin 'scrooloose/nerdcommenter'
Plugin 'Lokaltog/vim-powerline'
"状态栏
Plugin 'vim-airline/vim-airline'
Plugin 'vim-airline/vim-airline-themes'

Plugin 'rhysd/vim-clang-format'
call vundle#end()            " required
filetype plugin indent on    " required

"NERDTree 按下F2 调出/隐藏
nmap <silent> <F2> :execute 'NERDTreeToggle ' . getcwd()<CR>
autocmd vimenter * NERDTree
autocmd VimEnter * wincmd w
autocmd BufRead * NERDTree
autocmd BufRead * wincmd w


" 插入匹配括号
set showmatch 
""inoremap < <><LEFT>

" YouCompleteMe 功能
" 补全功能在注释中同样有效
let g:ycm_complete_in_comments=1
" 允许 vim 加载 .ycm_extra_conf.py 文件，不再提示
let g:ycm_confirm_extra_conf=0
" 开启 YCM 基于标签引擎
let g:ycm_collect_identifiers_from_tags_files=1
let g:ycm_global_ycm_extra_conf="~/.vim/bundle/YouCompleteMe/third_party/ycmd/cpp/ycm/.ycm_extra_conf.py"
" 引入 C++
"标准库tags，这个没有也没关系，只要.ycm_extra_conf.py文件中指定了正确的标准库路径
" set tags+=/data/misc/software/misc./vim/stdcpp.tags
" YCM 集成 OmniCppComplete 补全引擎，设置其快捷键
" inoremap <leader>; <C-x><C-o>
" 补全内容不以分割子窗口形式出现，只显示补全列表
"set completeopt-=preview
" 从第一个键入字符就开始罗列匹配项
let g:ycm_min_num_of_chars_for_completion=1
" 禁止缓存匹配项，每次都重新生成匹配项
let g:ycm_cache_omnifunc=0
" 语法关键字补全           
let g:ycm_seed_identifiers_with_syntax=1
" 修改对C函数的补全快捷键，默认是CTRL + space，修改为ALT + ;
"let g:ycm_key_invoke_completion = '<M-;>'
" 设置转到定义处的快捷键为ALT + G，这个功能非常赞
"nmap <M-g> :YcmCompleter GoToDefinitionElseDeclaration <C-R>=expand("<cword>")<CR><CR>
" 开启语义补全
let g:ycm_seed_identifiers_with_syntax=1
"autocmd InsertLeave * if pumvisible() == 0|pclose|endif
"let g:ycm_autoclose_preview_window_after_insertion=1
let g:ycm_autoclose_preview_window_after_completion = 1
let g:ycm_collect_identifiers_from_comments_and_strings = 1

nnoremap <leader>gl :YcmCompleter GoToDeclaration<CR>
nnoremap <leader>gf :YcmCompleter GoToDefinition<CR>
nnoremap <leader>gd :YcmCompleter GoToDefinitionElseDeclaration<CR>

"let g:solarized_termcolors=256
"let g:solarized_termtrans=1

let g:airline_powerline_fonts = 1
"let g:airline_theme='solarized'
let g:airline_theme='molokai'
let g:airline#extensions#tabline#enabled=1
let g:airline#extensions#tabline#left_sep = ' '
let g:airline#extensions#tabline#left_alt_sep = '|'

" ~/.vim/after/syntax/python.vim

syntax match TextSelf "\(\W\)\@<=self\(\W\)\@="
" this in Java is Type
" None in Python is Identifier
hi def link TextSelf Type

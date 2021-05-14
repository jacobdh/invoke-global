Global invoke scripts
======

Invoke is a cool tool for keeping your app/dir tasks together in a `tasks.py` file.
I also like to use it for global tasks to help me with things like AWS, docker, etc.

## Setup

1. Install [invoke](http://www.pyinvoke.org/installing.html) (I use pipx).

2. Add aliases for invoke, including a global version, to your zsh profile.
   The `--search-root` should be wherever you want to keep your global tasks
   (this repo).
```
alias i=invoke
invoke-global(){ invoke --search-root="$HOME/code/_invoke" "$@" }
alias ig=invoke-global
```

3. Add autocomplete scripts to your zsh profile:
```
    # Invoke completions
_complete_invoke() {
collection_arg=''
if [[ "${words}" =~ "(-c|--collection) [^ ]+" ]]; then
collection_arg=$MATCH
fi
reply=( $(invoke ${=collection_arg} --complete -- ${words}) )
}
_complete_invoke_global() {
collection_arg=''
if [[ "${words}" =~ "(-c|--collection) [^ ]+" ]]; then
collection_arg=$MATCH
fi
reply=( $(invoke-global ${=collection_arg} --complete -- ${words}) )
}
compctl -K _complete_invoke + -f invoke inv
compctl -K _complete_invoke_global + -f invoke-global ig
```

4. Run `ig --list` (from any directory) to see all the global tasks.

You can still use `i` or `invoke` inside a specific directory with a `tasks.py`
to run dir-specific tasks, which is the normal way invoke works.
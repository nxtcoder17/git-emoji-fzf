## git emoji fzf

### Needs to be installed
    - fzf
    - xclip

```sh
python main.py| fzf -d'\t' --with-nth '1..-2' | awk -F'\t' '{print $1}' | xclip -sel clip
```

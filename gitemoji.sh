selection=$(python main.py | fzf --reverse -d'\t' --with-nth '1..-2' | tr "\t" '|')

output=$(echo $selection | awk -F'|' '{print $1" "$2}')
echo $output copied to clipboard

code=$(echo $selection | awk -F'|' '{print $3}')

echo $code | tr -d '\n' | xclip -sel clip

notify-send "[$code] $output"

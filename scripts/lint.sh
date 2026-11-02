#!/usr/bin/env bash
# Check source files against the house style: 80 character lines, no trailing
# whitespace. URLs in markdown links cannot be wrapped, so lines whose overrun
# is entirely a link target are allowed.
set -uo pipefail

cd "$(dirname "$0")/.."

status=0

# Untracked files are checked too, so a new partial is not silently skipped.
files=$(git ls-files --cached --others --exclude-standard \
  '*.qmd' '*.css' '*.yml' '*.sh' | grep -v '^notes/')

for f in $files; do
  while IFS= read -r line; do
    n=${line%%:*}
    text=${line#*:}
    text=${text# }
    # A markdown link target cannot be wrapped, and a newline inside an ATX
    # heading ends the heading, splitting one slide into two. So lines
    # carrying a link, and headings themselves, are exempt.
    if [[ "$text" == *"http"* || "$text" == *"]("* || "$text" == "#"* ]]; then
      continue
    fi
    echo "$f:$n: line over 80 characters (${#text})"
    status=1
  done < <(awk 'length > 80 {print FNR": "$0}' "$f")

  while IFS= read -r hit; do
    echo "$f:${hit%%:*}: trailing whitespace"
    status=1
  done < <(grep -n '[[:space:]]$' "$f" 2>/dev/null)
done

if [ "$status" -eq 0 ]; then
  echo "lint: clean"
fi

exit "$status"

#!/usr/bin/env bash
# Fails if a secret (key, token, password, private key or .env file) is
# committed. Scans only files tracked by git. Test files, examples and
# docs are skipped because they contain fake values on purpose.
set -uo pipefail

EXCLUDE='(^|/)(node_modules|dist|docs|tests|\.venv)/|(^|/)test_[^/]*\.py$|\.example$|\.md$|\.docx$'

files=$(git ls-files | grep -Ev "$EXCLUDE")
found=0

report() {
  echo "SECRET FOUND [$1]: $2"
  found=1
}

# A real .env file must never be committed.
while IFS= read -r f; do
  [ -n "$f" ] && report "env-file" "$f is tracked by git"
done < <(git ls-files | grep -E '(^|/)\.env$')

# check NAME PATTERN [GREP_FLAGS]
check() {
  local name="$1" pattern="$2" flags="${3:-}"
  # shellcheck disable=SC2086
  while IFS= read -r hit; do
    [ -n "$hit" ] && report "$name" "$hit"
  done < <(echo "$files" | xargs grep -nIE $flags -e "$pattern" 2>/dev/null | cut -c1-200)
}

check "aws-access-key"   'AKIA[0-9A-Z]{16}'
check "private-key"      '-----BEGIN ([A-Z]+ )?PRIVATE KEY-----'
check "aidevops-api-key" 'aidv_(live|test)_[A-Za-z0-9_-]{20,}'
check "stripe-live-key"  'sk_live_[A-Za-z0-9]{16,}'
check "github-token"     'gh[pousr]_[A-Za-z0-9]{30,}'
check "hardcoded-secret" '(password|passwd|secret|api[_-]?key|jwt[_-]?secret)["'"'"']?[[:space:]]*[:=][[:space:]]*["'"'"'][^"'"'"'[:space:]]{8,}["'"'"']' -i

if [ "$found" -ne 0 ]; then
  echo
  echo "Remove the secret, rotate it, and load it from an environment variable instead."
  exit 1
fi
echo "No secrets found in $(echo "$files" | wc -l | tr -d ' ') tracked files."

import re
import sys

message = sys.argv[1]

MESSAGE_REGEX = re.compile(r"^#\d+\s(feat|fix|build|chore|ci|docs|style|refactor|perf|test|BREAKING_CHANGE):\s")

if not MESSAGE_REGEX.search(message):
    sys.exit(f"Invalid Commit Message: '{message}'")

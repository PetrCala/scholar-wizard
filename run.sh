#!/bin/bash

PROJECT_DIR_REL=$(dirname "${BASH_SOURCE[0]}")
source "$PROJECT_DIR_REL/scripts/shellUtils.sh"

PROJECT_ROOT="$(get_abs_path "$PROJECT_DIR_REL")"
SCRIPTS_DIR="$PROJECT_ROOT/scripts"

function run_lint {
  LINTRC_PATH="$PROJECT_ROOT/.pylintrc"
  LINT_PATH="$COMMANDER_CORE"
  TESTS_PATH="$PROJECT_ROOT/tests"
  pylint --recursive=y --rcfile="$LINTRC_PATH" "$LINT_PATH" "$TESTS_PATH" "$@"
}
function print_help {
  banner "                    Usage                    "
  echo "Available options: "
  echo "     lint             - Lint the folder"
  echo "     merge            - Merge the current branch into a specified one and push these changes to origin"
}

case ${1} in
lint)
  shift
  run_lint "$@"
  ;;
merge)
  shift
  source $SCRIPTS_DIR/mergeAndPush.sh "$@"
  ;;
*)
  echo "Got: ${1}"
  print_help
  ;;
esac

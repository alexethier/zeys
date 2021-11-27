#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

PROJECT_NAME="zeys"
SKIP_CLEANUP=false
INSTALL=true
TEST_DEPLOY=false
PROD_DEPLOY=false

while [[ $# > 0 ]]
do
    # ${1} is unbound so default it to ''
    key="${1-}"
    value="${2-}"

    # If arguments come in the form a=b
    if [[ $1 == *'='* ]]
    then
        IFS='=' read -ra key_pair <<< "$1"
        key="${key_pair[0]}"
        value="${key_pair[1]}"
    fi

    case $key in
        -s)
            SKIP_CLEANUP=true
            ;;
        --skip)
            SKIP_CLEANUP=true
            ;;
        -d)
            TEST_DEPLOY=true
            ;;
        --deploy)
            TEST_DEPLOY=true
            ;;
        -p)
            PROD_DEPLOY=true
            ;;
        --production)
            PROD_DEPLOY=true
            ;;
        -v)
            set -x
            ;;
        *)
            echo "Unknown option passed: $key"
            exit 1
            ;;
    esac
    shift
done

if [ "$INSTALL" == "true" ]; then
  pip install wheel
  pip list | tr -s ' ' | grep -e "^$PROJECT_NAME " | cut -d' ' -f1 | xargs -I {} pip uninstall -y {} || true
  python3 setup.py bdist_wheel
  ls -1 ./dist | grep -e ".whl$" | xargs -I {} pip install ./dist/{}
fi

if [ "$TEST_DEPLOY" == "true" ]; then
  echo "Uploading to test pypi"
  twine upload --repository testpypi dist/*
  pip list | tr -s ' ' | grep -e "^$PROJECT_NAME " | cut -d' ' -f1 | xargs -I {} pip uninstall -y {} || true
  echo "Reinstalling from test pypi"
  pip install --index-url https://test.pypi.org/simple/ $PROJECT_NAME
fi

if [ "$PROD_DEPLOY" == "true" ]; then
  echo "Uploading to Production PyPi"
  twine upload dist/*
  pip list | tr -s ' ' | grep -e "^$PROJECT_NAME " | cut -d' ' -f1 | xargs -I {} pip uninstall -y {} || true
  echo "Reinstalling from test pypi"
  pip install $PROJECT_NAME
fi

if [ "$SKIP_CLEANUP" == "false" ]; then
  rm -rf ./dist && rm -rf ./build && rm -rf "$PROJECT_NAME.egg-info"
fi

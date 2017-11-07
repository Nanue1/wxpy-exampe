find .. -name '*.pyc' | xargs rm -f
find .. -name 'log' | xargs rm -fr
find .. -name '__pycache__' | xargs rm -fr

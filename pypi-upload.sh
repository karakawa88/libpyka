#!/bin/bash

# 過去のパッケージのファイルを削除
rm -rf *.egg-info dist
# パッケージの作成
python3 setup.py sdist
python3 setup.py bdist_wheel
# PyPIにアップロード
twine upload --repository testpypi dist/*
twine upload --repository pypi dist/*


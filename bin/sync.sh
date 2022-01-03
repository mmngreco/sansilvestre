#!/usr/bin/env bash
# jupytext --set-formats py --sync analysis.ipynb
jupytext --to notebook --execute analysis.py
jupyter nbconvert --to html analysis.ipynb

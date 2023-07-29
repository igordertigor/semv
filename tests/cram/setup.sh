#!/bin/bash

git init 2> /dev/null
git config user.name "tester"
git config user.email "tester"
echo "This is the readme" > README.md
git add README.md
git commit -m 'docs(readme): Add readme'
git tag v0.0.0

#!/bin/bash

git add .
read -p "add some commit: " commit
git commit -m "$commit"
read -p "which branch did you want to push: " br
git push origin $br
exit 0


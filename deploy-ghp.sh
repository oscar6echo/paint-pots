#! /bin/bash

# make sure git is clear: git status --porcelain

git push origin --delete gh-pages
git branch -D gh-pages

git checkout --orphan gh-pages

git rm --cached -rf .


# gitignore to keep some items out of scope
# IMPORTANT: make sure items inside dist do not have same name
echo .gitignore > .gitignore
echo deploy-ghp.* >> .gitignore
echo dist >> .gitignore

# git clean -n
git clean -f

# bring dist to .
cp -rf dist/. .

# redirect
cp index.html 404.html


git add .
git commit -m "Deploy"
git push --set-upstream origin gh-pages

git checkout main

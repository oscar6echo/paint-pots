
REM make sure git is clear: git status --porcelain

git push origin --delete gh-pages
git branch -D gh-pages

git checkout --orphan gh-pages

git rm --cached -rf .


REM gitignore to keep some items out of scope
REM IMPORTANT: make sure items inside dist do not have same name
echo .gitignore > .gitignore
echo deploy-ghp.* >> .gitignore
echo dist >> .gitignore

REM git clean -n
git clean -f

REM bring dist to .
xcopy dist . /E /I /Y

REM redirect
copy index.html 404.html


git add .
git commit -m "Deploy"
git push --set-upstream origin gh-pages

git checkout main

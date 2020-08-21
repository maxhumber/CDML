### Deploy Flask to Heroku

1. Setup a virtual environment:

```
python -m venv .venv
```

2. Activate it:

```
source .venv/bin/activate
```

3. Install app and model dependencies (`gunicorn` is for in between the web and flask):

```
pip install gunicorn flask scikit-learn pandas sklearn_pandas
```

3. Freeze the dependencies:

```
pip freeze > requirements.txt
```

4. Retrain the model inside of the virtual environment:

```
python model.py
```

5. Make sure the app still works locally:

```
python app.py
```

6. Specify a python runtime (3.8 not working yet):

```
python --version
echo "python-3.7.9" > runtime.txt
```

7. Create a `Procfile`:

```
echo "web: gunicorn app:app --log-file -" > Procfile
```

8. If your project isn't already a git repo, make it one:

```
git init
touch .gitignore
echo ".venv" >> .gitignore
```

9. Login to Heroku from the [command line](https://devcenter.heroku.com/articles/heroku-cli):

```
heroku login
```

10. Create a project:

```
heroku create
```

11. Add a remote to the randomly generated project:

```
heroku git:remote -a silly-words-009900
```

12. Test the app locally:

```
heroku local
```

13. (Optional) Deactivate the virtual environment:

```
deactivate
```

14. add, commit push:

```
git add .
git commit -m '🚀'
git push heroku master
```

15. Click on the url and make sure it works!

16. (If something is wrong):

```
heroku logs -t 
```
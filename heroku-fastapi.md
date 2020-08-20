### Deploy Heroku 2 (fastAPI)

1. Setup a virtual environment:

```
python -m venv .venv
```

2. Activate it:

```
source .venv/bin/activate
```

3. Install app and model dependencies (`gunicorn` is for in between the web and flask):

   **NEW**

```
pip install uvicorn fastapi scikit-learn pandas sklearn_pandas
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

   **NEW**

```
echo "web: uvicorn app:app --workers=2" > Procfile
```

8. Test the app locally:

```
heroku local
```

9. add, commit push:

```
git add .
git commit -m '🚀'
git push heroku master
```

10. Click on the url and make sure it works!
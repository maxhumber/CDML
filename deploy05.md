#### Deploy: Dokku



Update environment

```
pip install tensorflow
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

6. Push everything up to GitHub:

```
git add .
git commit -m '🚀'
git push
```

7. Check logs (to make sure it all works)

```
dokku logs powerapp --tail
```

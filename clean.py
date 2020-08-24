import subprocess

subprocess.run(
    "rm -rf .DS_Store .venv app.py model.py pipe.pkl mapper.pkl model.h5 model.pkl requirements.txt runtime.txt Procfile utils.py",
shell=True)

subprocess.run("git remote rm dokku", shell=True)

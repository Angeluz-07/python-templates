# flask-demo
Demo to showcase flask basic features

## Set development environment
###  Windows
```
mkdir .venv
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```
###  Linux Based OS
```
mkdir .venv
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
````
### Set git hooks
```
pre-commit install -t pre-commit -t commit-msg
```

## Example usage in Windows
Run
```
set FLASK_APP=<app_folder>/app.py
flask run
```
Open `http://127.0.0.1:5000/`

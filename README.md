
[ProFitness]

Using Vanilla Javascript, Flask, SQLAlchemy(SQLite)

[Building and Running]
Use Python 3.8-3.10
To run the flask application, run these commands below
```
cd ProFitness

pip3 install -r requirements.txt

python3 app.py
```
after that, open the url:
http://localhost:8000/

Test the app with Demo ID/Password
```txt
Email: test123@gmail.com
Password: 0000000000
```

[Pip install throws error: externally-managed-environment]
```
mkdir ~/.venv
```
```
python3 -m venv ~/.venv
```
Creates the following in ~/.venv
		bin/
		include/
		lib/
		pyvenv.cfg does not create pip-selfcheck.json 

#### To activate the venv
```
source ~/.venv/bin/activate
```

#### Now you can..
```
python3 -m pip install <module name>
```

and it will install the module in the virtual env

#### to deactivate the venv
```
deactivate # or exit the shell
```

### Note:
You can chose any folder location and name that you want for the venv. ~/.venv is typical.
Your project code can be in any directory.


### Project Structure

```
.
├── README.md
├── empty.txt
├── fitness
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-38.pyc
│   │   ├── createplan.cpython-38.pyc
│   │   ├── database.cpython-38.pyc
│   │   ├── forms.cpython-38.pyc
│   │   └── routes.cpython-38.pyc
│   ├── createplan.py
│   ├── database.py
│   ├── forms.py
│   ├── routes.py
│   ├── site.db
│   ├── static
│   │   ├── css
│   │   ├── images
│   │   ├── img
│   │   ├── js
│   │   ├── music
│   │   ├── scss
│   │   ├── vendor
│   │   └── webfonts
│   └── templates
│       ├── base.html
│       ├── cardio.html
│       ├── clothes.html
│       ├── contact.html
│       ├── equipment.html
│       ├── exercise_search.html
│       ├── index copy.html
│       ├── index.html
│       ├── pomodoroTimer.html
│       ├── set_workout.html
│       ├── signin.html
│       ├── signup.html
│       ├── strength.html
│       ├── supplement.html
│       ├── todolist.html
│       ├── tracker.html
│       ├── user_dashboard.html
│       └── user_dashboard_template.html
│       ├── workout_detail.html
│       ├── workout_history.html
├── install.bat
├── install.sh
├── myapp
│   └── templates
│       └── user_dashboard.html
├── requirements.txt
└── app.py

14 directories, 35 files

```

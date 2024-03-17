# Expense Income Tracking (EXIN)

## Setup environment

_First make sure python and pip is installed on you machine, if not you can search how._

### Make your venv

Install venv

```bash
pip install virtualenv
```

Create env

```bash
python -m venv .venv
```

Active for windows (make sure the path is correct)

```bash
\.venv\Scripts\activate
```

Download the rebo

```bash
git clone https://github.com/ahmedhosam-dev/expense-income-tracking
```

Install all requirements from requirements.txt file

```bash
pip install -r requirements.txt
```

### Now lets set up our database server and SMTP host

I use postgresql check site [postgresql.org](https://www.postgresql.org/) and download it,

then create your database and add it info in .env file and SMTP host info you can search to know how to get it.

```bash
export SEC_KEY=<your_django_SECRET_KEY>

export DB_NAME=<Database_Name>
export DB_USER=<Database_UserName>
export DB_USER_PASSWORD=<Database_UserPassword>
export DB_HOST=<Database_Host_Name>

export EMAIL_HOST = <SMTP_Host>
export EMAIL_HOST_USER = <Email>
export DEFALUT_FORM_EMAIL = <Email>
export EMAIL_HOST_PASSWORD = <Email_APP_Password>

```

---

### Run app (make sure you in right path)

```bash
python manage.py runserver
```

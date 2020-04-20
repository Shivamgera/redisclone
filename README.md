## Steps to setup the project locally:

### For ubuntu, first clone/download the repo , switch to project directory

* sudo apt-get install python3-venv

* python3 -m venv env

* source env/bin/activate

* pip3 install -r requirements.txt

* python3 manage.py runserver

##### After setting up the project, you can use commands like GET, SET, EXPIRE, ZADD, ZRANK and ZRANGE.

* For SET use `/redis/`, in request.form enter `command=SET`, `key=<given_key>`, `value=<given_value`.

* For GET use `/redis/`, in request params enter `command=GET`, `key=<given_key>`.

* For EXPIRE use `/redis/expire/`, in request.form enter `command=EXPIRE`, `key=<given_key>`, `timeout=<given_seconds>`.


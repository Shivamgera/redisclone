## Steps to setup the project locally:

### For ubuntu, first clone/download the repo , switch to project directory

* sudo apt-get install python3-venv

* python3 -m venv env

* source env/bin/activate

* pip3 install -r requirements.txt

* python3 manage.py runserver

##### After setting up the project, you can use commands like GET, SET, EXPIRE, ZADD, ZRANK and ZRANGE.

* For SET use POST `/redis/`, in request.form enter `command=SET`, `key=<given_key>`, `value=<given_value>`.

* For GET use GET `/redis/`, in request params enter `command=GET`, `key=<given_key>`.

* For EXPIRE use POST `/redis/expire/`, in request.form enter `command=EXPIRE`, `key=<given_key>`, `timeout=<given_seconds>`.

* For ZADD use POST `/redis/zadd/`, in request.form enter `command=ZADD`, `key=<given_key>`, `value=<given_value>`, Eg- `value=1 uno 1 one`.

* For ZRANK use GET `/redis/zrank/`, in request params enter `command=ZRANK`, `key=<given_key>`, `value=<given_value>`, Eg- `value=uno`.

* For ZRANGE use GET `/redis/zrange/`, in request params enter `command=ZRANGE`, `key=<given_key>`, `start=<given_start>`, `stop=<given_stop>`, Eg- `start=0` , `stop=2`.

* To clear the cache use GET `/redis/clear/`.

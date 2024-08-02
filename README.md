Installation:

```
$ python -m venv venv \
&& . ./venv/bin/activate \
&& pip install -r requirements.txt
&& pip install -e .
```

Run:

```
$ python src/recanatid/main.py
```
or
```
$ recanatid [-h] [port]
```
Notes:

- Every startup uses generated random secret for JWT. Meaning that restarts invalidates all JWT tokens.

Steps:

1. Login with hardcoded credentials to obtain JWT: username=admin, password=secret

```
$ curl -sX POST -H Content-Type:application/json -d '{"username":"admin","password":"secret"}' http://127.0.0.1:8080/login | jq -r '.access_token'
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyMjM0MzIxNywianRpIjoiNTA4NTRhMDItMWVlNS00OGMxLTg0MjQtNGM4NDQ4N2RkOTdiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzIyMzQzMjE3LCJjc3JmIjoiMjBkZDk2ZTAtNmU4ZC00ZjMyLWExODctMTc0YTAxNTE2ZTZmIiwiZXhwIjoxNzIyMzQ0MTE3fQ.clp6THoKAeVNSQYLxu4dxRXhW0Fe-6rhY5oTeZ6QELA
```

2. Use access token to create new user

```
export TOKEN=$(curl -is -H Content-Type:application/json -H "Authorization: Bearer $(curl -sX POST -H Content-Type:application/json -d '{"username":"admin","password":"secret"}' http://127.0.0.1:8080/login | jq -r '.access_token')" -d '{"id":42, "name": "Daniel", "email": "daniel@daniel.com"}' http://127.0.0.1:8080/users)
```

3. Login a new user to obtain JWT

```
```

4. Use JWT to list users

```
curl -s -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8080/users
```
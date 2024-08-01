run:
	@python src/main.py

login:
	@curl -sX POST -H Content-Type:application/json -d '{"username":"admin","password":"secret"}' http://127.0.0.1:8080/login
get:
	@echo curl -sH "Authorization: Bearer $$\(curl -sX POST -H Content-Type:application/json -d '{"username":"admin","password":"secret"}' http://127.0.0.1:8080/login \| jq -r '.access_token')" http://127.0.0.1:8080/users/42
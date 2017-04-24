#How to deploy the server

- Clone the repository
- From server folder run `pip3 install -U -r flask`
- Copy config.py.example to config.py and fill the empty spaces
- Go to server/issues_monitoring and run `sudo env FLASK_APP=server.py python3 -m flask run`

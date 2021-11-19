.PHONY: run test certificate clean

run:
	sudo ./ssl-snitch.bt

test:
	make certificate
	python3 -m venv venv
	venv/bin/pip3 --quiet install requests 
	sudo venv/bin/python3 -m unittest test.py

certificate:
	openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 \
	        -out certificate.pem -subj "/CN=0.0.0.0/"

clean:
	rm -rf certificate.pem key.pem venv
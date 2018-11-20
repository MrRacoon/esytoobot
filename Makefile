.PHONY = build freeze start

activate:
	. ./env/bin/activate

build:
	pip3 install -r requirements.txt

freeze:
	pip3 freeze > requirements.txt

start:
	python3 src/starabot.py

from flask import Flask, render_template, request


app = Flask("frontend")

@app.get("/")
def index():
    contenx = dict()
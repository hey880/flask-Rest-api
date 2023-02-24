from flask import Flask

app = Flask(__name__)

@app.get("/hello")
def say_hello():
    return {"message":"Hello world"}


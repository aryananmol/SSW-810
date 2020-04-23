from flask import Flask, render_template
app: Flask = Flask(__name__)
@app.route ('/HELLO')
def hello():
    return "Hello this is flask"

app.run(debug=True)
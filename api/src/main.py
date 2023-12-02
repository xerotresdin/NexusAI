from flask import Flask

app = Flask(__name__)

@app.route('/')
def main():
    return 'hi mom'

@app.route('/analysis')
def parse_csv():


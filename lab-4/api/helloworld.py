from flask import Flask

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def index():
    return '<h1>Welcome page</h1>'

@app.route('/api/v1/hello-world-28')
def hello_world():
    return 'Hello, World 28!'

if __name__ == '__main__':
    app.run()
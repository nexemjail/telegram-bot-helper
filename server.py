from flask import Flask, jsonify, send_from_directory
from telegram_bot import start
import os

app = Flask(__name__, static_folder='Client')


index_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Client')
angular_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Client', 'libs')


@app.route('/')
@app.route('/index.html')
def root():
    #return send_from_directory(index_path, 'index.html')
    return app.send_static_file('index.html')


@app.route('/<path:path>', methods=['GET'])
def static_files(path):
    return send_from_directory('', path)

if __name__ == '__main__':
    # start()
    app.run(debug=True)


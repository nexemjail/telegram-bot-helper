from flask import Flask, jsonify, send_from_directory
from telegram_bot import start
import os

app = Flask(__name__, static_folder='Client')

root_path = os.path.dirname(os.path.abspath(__file__))
index_path = os.path.join(root_path, 'Client')
angular_path = os.path.join(root_path, 'Client', 'libs')


@app.route('/')
@app.route('/index.html')
def root():
    #return send_from_directory(index_path, 'index.html')
    return app.send_static_file('index.html')


@app.route('/<path:path>', methods=['GET'])
def static_files(path):
    return send_from_directory(root_path, path)


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    start()
    app.run(host='0.0.0.0', port=int(port), debug=True)
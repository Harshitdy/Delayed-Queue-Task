from flask import Flask, request, jsonify, render_template
import time
import os
import threading
from datetime import datetime, timedelta

app = Flask(__name__)
delayed_queue = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_item', methods=['POST'])
def add_item():
    data = request.get_json()
    item = data['item']
    delay = int(data['delay'])
    release_time = datetime.now() + timedelta(seconds=delay)
    delayed_queue.append({'item': item, 'release_time': release_time, 'shown': False})
    return jsonify({'msg': 'Item added to the delayed queue'})

@app.route('/show_items', methods=['GET'])
def show_items():
    current_time = datetime.now()
    items_to_show = sorted(
        [entry['item'] for entry in delayed_queue if entry['release_time'] <= current_time],
        key=lambda x: next(entry['release_time'] for entry in delayed_queue if entry['item'] == x)
    )
    for entry in delayed_queue:
        if entry['release_time'] <= current_time:
            entry['shown'] = True
    return jsonify(items_to_show)



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

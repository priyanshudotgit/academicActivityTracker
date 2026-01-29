from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

current_state = {
    "url": "",
    "browser_active": False
}

@app.route('/update-url', methods=['POST'])
def update_url():
    global current_browser_url
    
    # Store JSON data sent by the extension
    data = request.json
    
    if data and 'url' in data:
        current_state['url'] = data['url']
        # print(f"Browser looking at: {data['url']}")
        return jsonify({"status": "ok"}), 200
    
    return jsonify({"status": "error", "message": "No URL provided"}), 400

@app.route('/', methods=['GET'])
def health_check():
    return "academicActivityTracer Server is Running!"

if __name__ == '__main__':
    print("Server Running")
    app.run(port=5000, debug=True)
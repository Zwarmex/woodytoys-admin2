from flask import Flask
from datetime import datetime

app = Flask('time_service')

@app.route('/api/time', methods=['GET'])
def get_time():
    return f'misc: {datetime.now()}'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)


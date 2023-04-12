from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-program', methods=['POST'])
def run_program():
    # Get the request data (if any)
    request_data = request.get_json()

    # Check if the "start" key is in the request data
    if 'start' in request_data and 'hand' in request_data and request_data['start'] == True:
        # Launch the program as a subprocess
        print(request_data['hand'])
        subprocess.Popen(['python', '/Users/rohanmorar/Bia_Project/Bia/app/main.py', request_data['hand']], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Return a response indicating success
        return {'status': 'success'}
    else:
        # Return a response indicating failure
        return {'status': 'error', 'message': 'Invalid request data'}

if __name__ == '__main__':
    app.run()
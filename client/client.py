from flask import Flask, request, render_template,redirect,flash
import requests
import json

app = Flask(__name__)
app.template_folder = 'templates'

base_url = 'http://127.0.0.1:5000/Employees'

@app.route('/', methods=['GET'])
def index():
    response = requests.get(base_url)

    if response.status_code == 200:
        employees = response.json()
        return render_template('index.html', employees=employees)
    else:
        flash('Error connecting to the API')
    
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001) 
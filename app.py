from flask import Flask ,request ,render_template
from flask import jsonify
from flask_cors import CORS
import time
from utility import convert_ipynb_to_html
import os

app = Flask(__name__)
CORS(app)


@app.route('/' , methods=['GET'])
def get_status():
    return "Server Running" , 200

@app.route('/upload', methods=['POST'])
def print_notebook():
    if 'file' not in request.files:
        return jsonify({"message":"no file found"})
    file = request.files['file']
    # save it with a unique name in templates folder
    # return name of the file to the client
    # use millisecond to generate unique name
    filename = str(round(time.time())) 
    file.save('templates/' + filename + '.json')
    # convert the file to html
    # return the content of the html file to the client
    html_file_name = convert_ipynb_to_html('templates/' + filename+ '.json', 'templates/' + filename + '.html')
    # read html file and return the content
    with open(html_file_name, 'r' , encoding='utf-8') as f:
        html = f.read()
        os.remove('templates/' + filename+ '.json')
        # os.remove('templates/' + filename + '.html')
        return jsonify({"filename":filename+ '.html' , "content": "http://localhost:5000/render/"+filename + '.html' })

    return jsonify({"message":"something went wrong"})

@app.route('/render/<filename>', methods=['GET'])
def send_file(filename):
    return render_template(filename)

if __name__ == "__main__":
    app.run(debug=True)
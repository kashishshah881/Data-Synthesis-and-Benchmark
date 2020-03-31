from flask import Flask, render_template, request ,jsonify
import benchmarkfile as benfile
app = Flask(__name__)

@app.route('/')
def hello():
    return "Flask app is running"

@app.route('/synthesise', methods = ['POST', 'GET'])
def synthesise():
    if request.method == 'POST':
        content = request.json
        print(content)
        filename = content['filename']
        
        #dataset = content['json']
        print("filename = ", filename)
        #print("dataset = ", dataset)
        benfile.synthesise(filename)
        #full = url+dataset
    #base_url = 'metaflow-testing.s3.amazonaws.com/datasets/'
    #do synthesise here and return something 
        return "working"

if __name__ == '__main__':
    app.run(debug=True, host ='0.0.0.0')
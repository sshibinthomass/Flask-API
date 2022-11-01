from flask import *
import datetime
import json
import pickle
import numpy as np

app = Flask(__name__)
app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

courses = [
    {
        "Id": 1,
        "Name": "ABC",
        "Class": "5"
    },
    {
        "Id": 2,
        "Name": "DEF",
        "Class": "6"
    },
    {
        "Id": 3,
        "Name": "GHI",
        "Class": "6"
    }
]

@app.route('/')
def index():
    return 'Hello World'
# all Types
# GET
# http://127.0.0.1:5000/acourses

@app.route("/acourses", methods=['GET'])
def getCourse():
    return jsonify({'Courses': courses})

# http://127.0.0.1:5000/acourses/1

@app.route("/acourses/<int:course_id>", methods=['GET'])
def get_acourse(course_id):
    return jsonify({'course': courses[course_id]})


@app.route('/postCourse', methods=['POST'])
def post_course():
    post_data = request.get_json()
    courses.append(post_data)
    return "Success"


@app.route('/putcourse/<int:appId>', methods=['PUT'])
def put_course(appId):
    put_data = request.get_json()
    courses[appId]['Id'] = int(put_data['Id'])
    courses[appId]['Name'] = str(put_data['Name'])
    courses[appId]['Class'] = str(put_data['Class'])
    return "success"

@app.route('/deleteCourse/<int:appId>', methods=['DELETE'])
def delete_course(appId):
    courses.remove(courses[appId])
    return "Success"



# http://127.0.0.1:5000/sum/?numb1=45&numb2=67&opt=add
# add
# sub
# mul
# div
@app.route('/sum/', methods=['GET'])
def sum_page():
    opt = str(request.args.get('opt'))
    numb1 = int(request.args.get('numb1'))
    numb2 = int(request.args.get('numb2'))
    if(opt == "add"):
        val = numb1+numb2
    elif(opt == "sub"):
        val = numb1-numb2
    elif(opt == "mul"):
        val = numb1*numb2
    elif(opt == "div"):
        val = numb1/numb2
    else:
        val = 0
    data_set = {'value': val}
    json_dump = json.dumps(data_set)
    return json_dump

#http://127.0.0.1:5000/predict/?exp=4&Tscore=7&Iscore=4
@app.route('/predict/', methods=['GET'])
def predict():
    exp = int(request.args.get('exp'))
    Tscore = int(request.args.get('Tscore'))
    Iscore = int(request.args.get('Iscore'))
    final_features = [np.array([exp,Tscore,Iscore])]
    prediction = model.predict(final_features)
    output = round(prediction[0], 2)
    data_set = {'value': output}
    json_dump = json.dumps(data_set)
    return json_dump



#---------------------------------------------------------------------------------------------------------#
#WEB Application
# two decorators, same function
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', the_title='Tiger Home Page',utc_dt=datetime.datetime.utcnow())

@app.route('/symbol.html')
def symbol():
    return render_template('symbol.html', the_title='Tiger As Symbol')

@app.route('/myth.html')
def myth():
    return render_template('myth.html', the_title='Tiger in Myth and Legend')

@app.route('/comments.html')
def comments():
    comments = ['This is the first comment.',
                'This is the second comment.',
                'This is the third comment.',
                'This is the fourth comment.'
                ]

    return render_template('comments.html', comments=comments)

if __name__ == '__main__':
    app.run(debug=True)

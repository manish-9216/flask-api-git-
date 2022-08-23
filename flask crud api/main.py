from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://admin:admin@localhost/pets'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Record(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    name=db.Column(db.String(20),nullable=False)
    roll_no=db.Column(db.Integer(),nullable=False)
    stream=db.Column(db.String(20),nullable=False)



@app.route('/')
def index():
    return jsonify({'message':'Welcome to my site'})



@app.route('/add' ,  methods=['POST'])
def add():
    query=request.json

    name = query['name']
    roll_no = query['roll_no']
    stream = query['stream']

    data=Record(name=name,roll_no=roll_no,stream=stream)
    db.session.add(data)
    db.session.commit()


    return jsonify({"success": True,"response":"added"})


@app.route('/view' ,  methods=['GET'])
def view():
    query=Record.query.all()
    info=[]
    for i in query:
        results={

                    'id':i.id,
                    'name':i.name,
                    'roll_no':i.roll_no,
                    'stream':i.stream
        }

        info.append(results)

    return jsonify(
            {
                "success": True,
                "pets": info,
                "total_pets": len(query)
            }
        )


@app.route("/update/<int:pk>", methods = ["PATCH"])
def update(pk):
    query = Record.query.get(pk)
    name = request.json['name']
    roll_no = request.json['roll_no']
    stream = request.json['stream']


    if query is None:
        print("not found")
    else:
        query.name = name
        query.roll_no = roll_no
        query.stream = stream
        db.session.add(query)
        db.session.commit()
        return jsonify({"success": True, "response": "Details updated"})





if __name__ == '__main__':
    # db.create_all()

    app.run(debug=True)
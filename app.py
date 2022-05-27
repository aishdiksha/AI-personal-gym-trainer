from flask import Flask, render_template, jsonify
from sqlalchemy import create_engine
app = Flask(__name__)
from leg import start_leg_excercise 
from knee import start_knee_excercise
from database import  ArmExercise,LegExercise,KneeExercise
from arms import start_arm_excercise
from sqlalchemy.orm import sessionmaker 

def opendb():
    engine = create_engine('sqlite:///db.sqlite3')
    Session = sessionmaker(bind=engine)
    sess = Session()
    return sess

@app.route('/')
def index():
    db = opendb()
    if not db.query(ArmExercise).filter(ArmExercise.user_id == 1).first():
        db.add(ArmExercise(counter=0))
    else:
        print("Arm exercise already exists")
    if not db.query(LegExercise).filter(LegExercise.user_id == 1).first():
        db.add(LegExercise(counter=0))
    else:
        print("Leg exercise already exists")
    if not db.query(KneeExercise).filter(KneeExercise.user_id == 1).first():
        db.add(KneeExercise(counter=0))
    else:
        print("Knee exercise already exists")

    db.commit()
    db.close()
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    db = opendb()
    armExerciseData = db.query(ArmExercise).all()[-1]
    legExerciseData = db.query(LegExercise).all()[-1]
    kneeExerciseData = db.query(KneeExercise).all()[-1]
    db.close()
    return render_template('dashboard.html', arms= armExerciseData, leg = legExerciseData, knee = kneeExerciseData)

@app.route('/arms')
def arms():
    start_arm_excercise()
    return jsonify(success=True)

@app.route('/leg')
def leg():
    start_leg_excercise()
    return jsonify(success=True)

@app.route('/knee')
def knee():
    start_knee_excercise()
    return jsonify(success=True)


if __name__ == '__main__':
    app.run(debug=True)
 
from flask import Flask, render_template, request, redirect, url_for
from models import db, Appointment
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    try:
        db.create_all()
        print("Database and tables created successfully.")
    except Exception as e:
        print(f"Error creating database: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if request.method == 'POST':
        name = request.form['name']
        time = request.form['time']
        new_appointment = Appointment(name=name, time=time)
        db.session.add(new_appointment)
        db.session.commit()
        return redirect(url_for('appointments'))
    appointments = Appointment.query.all()
    return render_template('appointments.html', appointments=appointments)

@app.route('/queue')
def queue():
    appointments = Appointment.query.order_by(Appointment.time).all()
    return render_template('queue.html', appointments=appointments)

if __name__ == '__main__':
    # Check if the database file exists
    if not os.path.exists('database.db'):
        print("Database file does not exist, creating it.")
    else:
        print("Database file exists.")
    
    app.run(debug=True)
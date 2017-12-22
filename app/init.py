from datetime import datetime
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////data/LDR_readings.db'
db = SQLAlchemy(app)

# Declare Model
class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    stamp = db.Column(db.DateTime)

    def __init__(self, value, stamp=None):
        self.value = value
        if stamp is None:
            stamp = datetime.utcnow()
        self.stamp = stamp

    def __repr__(self):
        return '<Post %r>' % self.title

db.create_all()

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
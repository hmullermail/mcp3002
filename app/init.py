from datetime import datetime
from flask import Markup
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
        #return '<Value %r>' % self.value
        return '%r' % self.value
    
def count_logs():
    return db.session.query(Reading).count()


def reading_logs(points):
  #print str(Reading.query.all())
  read = Reading.query.filter_by(id=points).first()
  print read

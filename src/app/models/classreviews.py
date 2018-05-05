from . import *

class ClassReview(Base):
  __tablename__ = 'classreviews'

  id = db.Column(db.Integer, primary_key=True)
  class_name = db.Column(db.String(255))
  prof_name = db.Column(db.String(255))
  review = db.Column(db.Text)
  difficulty = db.Column(db.Integer)
  content_quality = db.Column(db.Integer)



  def __init__(self, **kwargs):
    self.class_name = kwargs.get('class_name')
    self.prof_name = kwargs.get('prof_name')
    self.review = kwargs.get('review')
    self.difficulty = kwargs.get('difficulty')
    self.content_quality = kwargs.get('content_quality')

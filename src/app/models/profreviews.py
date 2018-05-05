from . import *

class ProfReview(Base):
  __tablename__ = 'profreviews'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255))
  class_name = db.Column(db.String(255))
  review = db.Column(db.Text)
  difficulty = db.Column(db.Integer)
  teaching_quality = db.Column(db.Integer)


  def __init__(self, **kwargs):
    self.name = kwargs.get('name')
    self.class_name = kwargs.get('class_name')
    self.review = kwargs.get('review')
    self.difficulty = kwargs.get('difficulty')
    self.teaching_quality = kwargs.get('teaching_quality')

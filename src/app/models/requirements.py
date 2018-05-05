from . import *

class Requirements(Base):
  __tablename__ = 'requirements'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255))
  distribution_name = db.Column(db.String(255))
  credits = db.Column(db.Integer)
  req_class = db.Column(db.Text)
  class_level = db.Column(db.Integer)


  def __init__(self, **kwargs):
    self.name = kwargs.get('name')
    self.distribution_name = kwargs.get('distribution_name')
    self.credits = kwargs.get('credits')
    self.req_class = kwargs.get('req_class')
    self.class_level = kwargs.get('class_level')

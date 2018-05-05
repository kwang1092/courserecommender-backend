from . import *
from flask import jsonify, request

class GetClassReviewsController(AppDevController):

  def get_path(self):
    return '/class_reviews'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    class_name = request.args.get('name')
    class_name = class_name.lower().strip().replace(' ','')
    reviews = class_dao.get_class_reviews(class_name)
    return [class_dao.serialize_reviews(review) for review in reviews]

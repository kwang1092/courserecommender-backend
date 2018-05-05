from . import *
from flask import jsonify, request


class GetProfReviewsController(AppDevController):

  def get_path(self):
    return '/prof_reviews'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    prof_name = request.args.get('name')
    prof_name = prof_name.lower().strip().replace(' ','')
    reviews = prof_dao.get_prof_reviews(prof_name)
    return [prof_dao.serialize_reviews(review) for review in reviews]

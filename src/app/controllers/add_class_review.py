from . import *
from flask import jsonify, request


class AddClassReviewController(AppDevController):

  def get_path(self):
    return '/make_class_review'

  def get_methods(self):
    return ['POST']

  def content(self, **kwargs):
    class_name = request.args.get('class_name')
    class_name = class_name.lower().strip().replace(' ','')
    prof_name = request.args.get('prof_name')
    review = request.args.get('review')
    difficulty = request.args.get('difficulty')
    quality = request.args.get('quality')
    class_dao.create_review(class_name,prof_name, review, difficulty, quality)
    return {"Success": "True"}

from . import *
from flask import jsonify, request


class AddProfReviewController(AppDevController):

  def get_path(self):
    return '/make_prof_review'

  def get_methods(self):
    return ['POST']

  def content(self, **kwargs):
    name = request.args.get('name')
    name = name.lower().strip().replace(' ','')
    class_name = request.args.get('class_name')
    review = request.args.get('review')
    difficulty = request.args.get('difficulty')
    quality = request.args.get('quality')
    prof_dao.create_review(name,class_name, review, difficulty, quality)
    return {"Success": "True"}

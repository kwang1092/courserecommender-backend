from . import *
from flask import jsonify, request

class GetMajorReqsController(AppDevController):

  def get_path(self):
    return '/major_reqs'

  def get_methods(self):
    return ['GET']

  def content(self, **kwargs):
    major_name = request.args.get('name')
    major_name = major_name.lower().strip().replace(' ','')
    reqs = requirements_dao.get_major_requirements(major_name)
    return [requirements_dao.serialize_reqs(req) for req in reqs]

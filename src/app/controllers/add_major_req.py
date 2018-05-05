from . import *
from flask import jsonify, request


class AddMajorReqController(AppDevController):

  def get_path(self):
    return '/add_major_req'

  def get_methods(self):
    return ['POST']

  def content(self, **kwargs):
    name = request.args.get('name')
    name = name.lower().strip().replace(' ','')
    distribution_name = request.args.get('distribution_name')
    credits = request.args.get('credits')
    req_class = request.args.get('req_class')
    if req_class is None:
        req_class = ""
    class_level = request.args.get('class_level')
    if class_level is None:
        class_level = 100000
    requirements_dao.create_req(name,distribution_name, credits,req_class,class_level)
    return {"Success": "True"}

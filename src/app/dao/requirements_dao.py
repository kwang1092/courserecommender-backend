from . import *

def get_major_requirements(major_name):
  return Requirements.query.filter(Requirements.name==major_name).all()

def create_req(name,distribution_name, credits,req_class,class_level):
  reqs = Requirements(
      name=name,
      distribution_name=distribution_name,
      credits=credits,
      req_class=req_class,
      class_level=class_level
  )
  db_utils.commit_model(reqs)
  return True, reqs

def serialize_reqs(reqs):
    return requirements_schema.dump(reqs).data

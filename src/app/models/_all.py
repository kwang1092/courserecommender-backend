from marshmallow_sqlalchemy import ModelSchema

from app.models.user import *
from app.models.classreviews import *
from app.models.profreviews import *
from app.models.requirements import *


class UserSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = User

class ProfSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = ProfReview

class ClassSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = ClassReview

class RequirementsSchema(ModelSchema):
  class Meta(ModelSchema.Meta):
    model = Requirements



prof_schema = ProfSchema()
class_schema = ClassSchema()
requirements_schema = RequirementsSchema()

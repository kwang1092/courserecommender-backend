from flask import request, render_template, jsonify, redirect
from appdev.controllers import *

from app.dao import users_dao
from app.dao import prof_dao
from app.dao import class_dao
from app.dao import requirements_dao


from app.models._all import *

# # serializers
# user_schema = UserSchema()

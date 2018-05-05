from app.controllers.hello_world import HelloWorldController
from app.controllers.add_class_review import *
from app.controllers.add_prof_review import *
from app.controllers.get_class_reviews import *
from app.controllers.get_prof_reviews import *
from app.controllers.add_major_req import *
from app.controllers.get_major_reqs import *
from app.controllers.get_classes import *


controllers = [
    HelloWorldController(),
    AddProfReviewController(),
    GetClassReviewsController(),
    GetProfReviewsController(),
    AddClassReviewController(),
    GetMajorReqsController(),
    AddMajorReqController(),
    GetClassesController()

]

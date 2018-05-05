from . import *

def get_class_reviews(class_name):
  return ClassReview.query.filter(ClassReview.class_name== class_name).all()

def create_review(class_name,prof_name, review, difficulty, quality):
  review = ClassReview(
      class_name=class_name,
      prof_name=prof_name,
      review=review,
      difficulty=difficulty,
      content_quality=quality
  )
  db_utils.commit_model(review)
  return True, review


def serialize_reviews(reviews):
  return class_schema.dump(reviews).data

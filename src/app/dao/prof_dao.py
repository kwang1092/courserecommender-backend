from . import *

def get_prof_reviews(prof_name):
  return ProfReview.query.filter(ProfReview.name==prof_name).all()

def create_review(name,class_name, review, difficulty, quality):
  review = ProfReview(
      name=name,
      class_name=class_name,
      review=review,
      difficulty=difficulty,
      teaching_quality=quality
  )
  db_utils.commit_model(review)
  return True, review

def serialize_reviews(reviews):
    return prof_schema.dump(reviews).data

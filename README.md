Course recommender backend
We set up an sql database that has 3 tables to store reviews for classes and professors, and also to store the requirements needed to graduate for different majors.

Currently we have fully functional (but not deployed) endpoints that do the following actions:
Class Reviews:
1. Add Class Reviews (localhost:5000/api/v0/make_class_review?class_name=cs3110&prof_name=foster&review=amazing&difficulty=3&quality=5)
2. Get Class Reviews (localhost:5000/api/v0/class_reviews?name=cs3110)

Professor reviews:
1. Get Professor Reviews (localhost:5000/api/v0/prof_reviews?name=bob)
2. Add Professor Reviews (localhost:5000/api/v0/make_prof_review?class_name=%22john%22&review=%22horrible%22&difficulty=1&quality=2)

Requirements:
1. Get All the Requirments for a major (localhost:5000/api/v0/major_reqs?name=csarts)
2. Add new requirments for a major  (localhost:5000/api/v0/add_major_req?name=csArts&distribution_name=STATS&credits=4&req_class=btry3080,cs4850,ece3100,econ3130,engrd2700,math4710)

Get Classes:
1. This end point takes a list of all the classes that the student has taken at Cornell, and their major and then returns a list of the requirments that they have fulfilled, requirements that they need to fulfill, and the list of classes that they can use to fulfill those requiremnts. To do this we used our requirments table and also made api calls to the codi database to get class informationn. (localhost:5000/api/v0/getClasses?major=csarts&classes_taken=cs 2110,cs 3410)

All of the end points worked locally, however we were unable to deploy properly.

Course recommender backend
We set up an sql database that has 3 tables to store reviews for classes and professors, and also to store the requirements needed to graduate for different majors.

Currently we have fully functional (but not deployed) endpoints that do the following actions:
Class Reviews:
1. Add Class Reviews
2. Get Class Reviews

Professor reviews:
1. Get Professor Reviews
2. Add Professor Reviews

Requirements:
1. Get All the Requirments for a major
2. Add new requirments for a major 

Get Classes:
1. This end point takes a list of all the classes that the student has taken at Cornell, and their major and then returns a list of the requirments that they have fulfilled, requirements that they need to fulfill, and the list of classes that they can use to fulfill those requiremnts. To do this we used our requirments table and also made api calls to the codi database to get class informationn.

All of the end points worked locally, however we were unable to deploy properly.

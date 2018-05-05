from . import *
from flask import jsonify, request
import requests


class GetClassesController(AppDevController):

  def get_path(self):
    return '/getClasses'

  def get_methods(self):
    return ['GET']

  def get_subjects(self):
    r = requests.get("https://classes.cornell.edu/api/2.0/config/subjects.json?roster=FA18")
    json = r.json()
    data = json['data']
    subjects = data['subjects']
    acc = []
    for subj in subjects:
       acc.append(subj["value"])
    return acc

  def get_class_roster(self,subjects):
    acc =[]
    for subject in subjects:
      try:
        r = requests.get("https://classes.cornell.edu/api/2.0/search/classes.json?roster=FA18&subject="+subject)
        json = r.json()
        data = json["data"]
        classes = data["classes"]
        for cla in classes:
          cname = cla["subject"]+" " + cla["catalogNbr"]
          title = cla["titleLong"]
          description = cla["description"]
          dist = cla["catalogDistr"]
          try:
            firstname = cla["enrollGroups"][0]["classSections"][0]["meetings"][0]["instructors"][0]["firstName"]
            lastname = cla["enrollGroups"][0]["classSections"][0]["meetings"][0]["instructors"][0]["lastName"]
            profname = firstname + " " + lastname
          except Exception as e:
              profname = ""
          acc.append({"class":cname,"title":title,"description":description,"dist":dist,"prof":profname})
      except Exception as e:
        acc=acc
    return acc

  def get_class_for_dist(self,classes,dist):
    acc =[]
    for cl in classes:
        if(cl["dist"]!=None and dist in cl["dist"]):
            acc.append(cl)
    return acc

  def in_list(self,lst,name):
    for cl in lst:
      if cl["class"].lower() == name.lower():
        return True
    return False

  def get_4000(self,classes):
    acc =[]
    for cl in classes:
      if("CS 4" in cl["class"] or "CS 5" in cl["class"]):
        acc.append(cl)
    return acc

  def content(self, **kwargs):
    classes= self.get_class_roster(self.get_subjects())
    major_name = request.args.get('major')
    major_name = major_name.lower().strip().replace(' ','')
    mqr = self.get_class_for_dist(classes,"MQR")
    pbs = self.get_class_for_dist(classes,"PBS")
    sba = self.get_class_for_dist(classes,"SBA-AS")
    la = self.get_class_for_dist(classes,"LA-AS")
    kcm = self.get_class_for_dist(classes,"KCM-AS")
    ha = self.get_class_for_dist(classes,"HA-AS")
    ca = self.get_class_for_dist(classes,"CA-AS")
    fourT = self.get_4000(classes)
    classes_taken = request.args.get('classes_taken').split(",")
    json = {"completed":[],"incomplete":[]}
    reqs = requirements_dao.get_major_requirements(major_name)
    reqs = [requirements_dao.serialize_reqs(req) for req in reqs]
    for cla in classes_taken:
      found = False
      class_name = cla.lower().strip().replace(' ','')
      space = cla.strip().find(" ")
      class_code = cla[:space]
      class_number = int(cla[space + 1:])
      for req in reqs:
        if(not found):
          name = req["distribution_name"]
          req_class = req["req_class"]
          possible_classes = req_class.split(",")
          req_level = req["class_level"]
          for pc in possible_classes:
            if(pc.lower().strip().replace(' ','') == class_name):
              json["completed"].append({"requirement":name,"class_taken":cla.upper()})
              reqs.remove(req)
              found = True
              break
      if(not found):
        for req in reqs:
          name = req["distribution_name"]
          req_class = req["req_class"]
          req_level = req["class_level"]
          if(class_code.lower()=="cs" and class_number>=req_level and (not found)):
            json["completed"].append({"requirement":name,"class_taken":cla.upper()})
            reqs.remove(req)
          elif(name == "MQR" and self.in_list(mqr,cla)):
            json["completed"].append({"requirement":name,"class_taken":cla.upper()})
            reqs.remove(req)
          elif(name == "PBS" and self.in_list(pbs,cla)):
            json["completed"].append({"requirement":name,"class_taken":cla.upper()})
            reqs.remove(req)
          elif(name == "SBA-AS" and self.in_list(sba,cla)):
            json["completed"].append({"requirement":name,"class_taken":cla.upper()})
            reqs.remove(req)
          elif(name == "LA-AS" and self.in_list(la,cla)):
            json["completed"].append({"requirement":name,"class_taken":cla.upper()})
            reqs.remove(req)
          elif(name == "KCM-AS" and self.in_list(kcm,cla)):
            json["completed"].append({"requirement":name,"class_taken":cla.upper()})
            reqs.remove(req)
          elif(name == "HA-AS" and self.in_list(ha,cla)):
            json["completed"].append({"requirement":name,"class_taken":cla.upper()})
            reqs.remove(req)
          elif(name == "CA-AS" and self.in_list(ca,cla)):
            json["completed"].append({"requirement":name,"class_taken":cla.upper()})
            reqs.remove(req)
    for req in reqs:
      name = req["distribution_name"]
      req_class = req["req_class"]
      req_level = req["class_level"]
      if(len(req_class)>0):
        required_class = req_class.split(",")
        json["incomplete"].append({"requirement":name,"required_class":required_class, "suggested_classes":[]})
        reqs.remove(req)
      elif(name.replace(' ','') == "CS4000"):
        json["incomplete"].append({"requirement":name,"required_class":[], "suggested_classes":fourT})
        reqs.remove(req)
      elif(name == "MQR"):
        json["incomplete"].append({"requirement":name,"required_class":[], "suggested_classes":mqr})
        reqs.remove(req)
      elif(name == "PBS"):
        json["incomplete"].append({"requirement":name,"required_class":[], "suggested_classes":pbs})
        reqs.remove(req)
      elif(name == "SBA-AS"):
        json["incomplete"].append({"requirement":name,"required_class":[], "suggested_classes":sba})
        reqs.remove(req)
      elif(name == "LA-AS"):
        json["incomplete"].append({"requirement":name,"required_class":[], "suggested_classes":la})
        reqs.remove(req)
      elif(name == "KCM-AS"):
        json["incomplete"].append({"requirement":name,"required_class":[], "suggested_classes":kcm})
        reqs.remove(req)
      elif(name == "HA-AS"):
        json["incomplete"].append({"requirement":name,"required_class":[], "suggested_classes":ha})
        reqs.remove(req)
      elif(name == "CA-AS"):
        json["incomplete"].append({"requirement":name,"required_class":[], "suggested_classes":ca})
        reqs.remove(req)
    return json

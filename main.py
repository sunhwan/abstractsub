#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import cgi
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from models import *
import os
from google.appengine.ext import db

class MainHandler(webapp.RequestHandler):
    def get(self):
        faculties = Faculty().all().order('lastname')
        students = Student().all().order('lastname')
        people = Person().all().order('lastname')
        abstracts = Abstract().all().order('-date')
        
        template_values = {
            'faculties': faculties,
            'students': students,
            'abstracts': abstracts,
            'people': people
        }
        
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class SubmissionHandler(webapp.RequestHandler):
    def post(self):
        abstract = Abstract()
        abstract.title = cgi.escape(self.request.get('title'))
        abstract.authors = cgi.escape(self.request.get('authors'))
        present_by_key = cgi.escape(self.request.get('present_by'))
        abstract.present_by = db.get(db.Key(present_by_key))
        abstract.abstract = cgi.escape(self.request.get('abstract'))
        abstract.put()
        
        abstract.present_by.abstracts += 1
        if abstract.present_by.mentor:
            abstract.present_by.mentor.abstract += 1
        abstract.put()
        self.redirect("/")

def main():
  application = webapp.WSGIApplication([('/', MainHandler),
                                        ('/submit', SubmissionHandler),
                                       ], debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()

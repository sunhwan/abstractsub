from models import *
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('clearing data store')
        self.response.out.write('<p>')
        
        persons = Person.all()
        for p in persons: p.delete()
        abstracts = Abstract.all()
        for a in abstracts: a.delete()

        self.response.out.write('updating faculty information')
        self.response.out.write('<p>')
                
        import urllib2, re
        uris = ['index.shtml', 'index_gq.shtml', 'index_rz.shtml']
        base_url = 'http://www.molecularbiosciences.ku.edu/~mb/faculty'
        for uri in uris:
            fp = urllib2.urlopen('%s/%s' % (base_url, uri))
            _name = re.compile(r'viewprofile.shtml\?id=.*">(?P<firstname>.*) (?P<lastname>.*)</a')
            _email = re.compile(r'username = "(?P<email>.*)"')
            html = fp.read()
            names = _name.findall(html)
            emails = _email.findall(html)
            for i in range(len(names)):
                faculty = Faculty()
                faculty.firstname = names[i][0]
                faculty.lastname = names[i][1]
                faculty.email = '%s@ku.edu' % emails[i]
                faculty.put()

        self.response.out.write('updating student information')
        self.response.out.write('<p>')
        
        fp = urllib2.urlopen('http://www.molecularbiosciences.ku.edu/~mb/students/index.shtml')
        html = fp.read()
        _block = re.compile(r'<tr .*?class="style7">(.*?)</tr>', re.DOTALL)
        _td = re.compile(r'<td>(.*)</td>')
        blocks = _block.findall(html)
        for block in blocks:
            cells = _td.findall(block)
            name = cells[0]
            focus = cells[1]
            mentor = cells[2]
            phone = cells[3]
            lab = cells[4]
            email = cells[5]

            lastname, firstname = name.split(', ')
            student = Student()
            student.firstname = firstname
            student.lastname = lastname
            if email:
                student.email = email

            if mentor and mentor.find(',') != -1:
                mlastname, mfirstname = mentor.split(', ')
                s = Faculty.gql("WHERE lastname = :1 and firstname = :2", mlastname, mfirstname)
                if s: student.mentor = s.get()

            student.put()
        
        self.response.out.write('updating test abstract')
        self.response.out.write('<p>')
        
        abstract = Abstract()
        abstract.title = 'NMR characterization of the inner rod proteins of the bacterial needle apparatus'
        abstract.authors = 'Dalian Zhong, Sunhwan Jo, Yu Wang, Chet W. Egan, Roberto N. De Guzman'
        abstract.abstract = 'Many bacterial pathogens require a type III secretion needle apparatus to cause a wide variety of human diseases.  The needle apparatus is a syringe-like protein assembly used by pathogens to inject virulence factors into their hosts to initiate infection.  It consists of a base anchored at the bacterial membrane, a surface exposed needle, and a tip complex in contact with the host membrane.  In Salmonella typhimurium, the inner rod protein PrgJ is thought to assemble inside the base and contact the needle.  PrgJ is important in virulence as evidenced by the non-invasive phenotype of a PrgJ knockout strain.  Although PrgJ is an important component of the needle apparatus, there is little knowledge regarding the biophysical and structural properties of PrgJ and other inner rod proteins. This is due to self-polymerization of the inner rod proteins, which leads to aggregation, and preclude further biophysical studies.  When attached to GB1, the B1 immunoglobulin-binding domain of Streptococcus protein G, PrgJ and other needle rod proteins are soluble, thus, allowing characterization by NMR, CD, and fluorescence spectroscopies.  To validate this approach, we also attached GB1 to the needle proteins, which are also self-polymerizing proteins involved in needle assembly, but with known biophysical and structural data.  We show that GB1 fusion does not alter the structures and allows studies of protein-protein interactions of needle proteins by NMR.  Thus, fusion with GB1 is a valid approach in determining the NMR structures, biophysical properties, and protein-protein interactions of self-polymerizing proteins involved in type III secretion.'
        student = Student.gql("WHERE lastname = :1 and firstname = :2", 'Jo', 'Sunhwan').get()
        abstract.present_by = student
        abstract.put()
    
application = webapp.WSGIApplication([('/fixtures', MainPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
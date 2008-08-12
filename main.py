import cgi
import wsgiref.handlers
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

class User(db.Model):
  browser_ip    = db.StringProperty( required = True )
  host          = db.StringProperty()
  name          = db.StringProperty( required = True )
  key_type      = db.StringProperty( required = True )
  public_key    = db.TextProperty( required = True )
  number        = db.IntegerProperty( required = True )
  length        = db.IntegerProperty( required = True )
  
  date = db.DateTimeProperty( auto_now_add = True )

  def __init__(self, *args, **keywords):
    if keywords.has_key('public_key_dump'):
      data = keywords.pop('public_key_dump').strip().split()
      keywords['key_type'] = data[0]
      keywords['number'] = long(data[1])
      keywords['length'] = long(data[2])
      keywords['name'] = data[3]
      keywords['public_key'] = "\n".join(data[4:-1])
    
    super(User, self).__init__(*args, **keywords)

class AddKey(webapp.RequestHandler):
  def post(self):
    try:
      user = User(
        browser_ip      = self.request.remote_addr,
        public_key_dump = self.request.get('public_key'),
        host            = self.request.get('host')
      )

      user.put()
    except:
      pass
      
    self.redirect('/')

class MainPage(webapp.RequestHandler):
  def get(self):
    user_query = User.all().order('-date')
    users = user_query.fetch(1000)

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, {'users': users}))

def main():
  application = webapp.WSGIApplication(
                                       [('/', MainPage),
                                        ('/add', AddKey)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

    
if __name__ == "__main__":
  main()

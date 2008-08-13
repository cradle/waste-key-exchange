import cgi
import wsgiref.handlers
import os
from parser import Key
from StringIO import StringIO
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

class User(db.Model):
  browser_ip    = db.StringProperty( required = True )
  host          = db.StringProperty()
  name          = db.StringProperty( required = True )
  key_type      = db.StringProperty( required = True )
  network_name  = db.StringProperty()
  public_key    = db.TextProperty( required = True )
  number        = db.IntegerProperty( required = True )
  length        = db.IntegerProperty( required = True )
  
  date = db.DateTimeProperty( auto_now_add = True )
  
  def create_from_file(file, **v):
    num = 0
    
    try:
      while(1):
        k = Key(file)
        u = User(
          public_key = "\n".join(k.public),
          name         = k.name,
          length       = k.length,
          number       = k.number,
          network_name = v['network_name'],
          browser_ip   = v['browser_ip'],
          host         = v['host'],
          key_type     = Key.token,
        )
        u.put()
        num += 1
    except StopIteration:
      pass
      
    return num 
  create_from_file = staticmethod(create_from_file)

class AddKey(webapp.RequestHandler):
  def post(self):
    User.create_from_file(
      StringIO(self.request.get('public_keys')),
      network_name    = self.request.get('network'),
      browser_ip      = self.request.remote_addr,
      host            = self.request.get('host')
    )
      
    self.redirect('/')

class MainPage(webapp.RequestHandler):
  def get(self):
    users = User.all().filter('network_name =', '').order('-date').fetch(1000)

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

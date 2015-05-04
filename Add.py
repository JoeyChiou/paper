﻿from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import webapp2
import sys
import datetime


AddPage_HTML = """\
<html>
	<body>
		<form action="/Add/add" method="post">
			<div>Publish year:<br><input name="publish_year" rows="3" cols="60"></input></div>
			<div>Source:<br><input name="source" rows="3" cols="60"></input></div>
			<div>Title:<br><input name="title" rows="3" cols="60"></input></div>
			<div><input type="submit" value="add"></div>
		</form>
	</body>
</html>

"""

Add_HTML = """\
<html>
	<body>
		<form action="%s" method="post" enctype="multipart/form-data">
		Upload File: 	<input type="file" name="file"><br>
						<input type="submit" name="submit" value="Upload"> 
		</form>
	</body>
</html>

"""

class Paper(ndb.Model):
	title = ndb.StringProperty()
	source = ndb.StringProperty()
	name = ndb.StringProperty()
	time = ndb.DateTimeProperty(auto_now_add=True)
	publish_year = ndb.StringProperty()
	
class AddPage(webapp2.RequestHandler):
	def post(self):
		self.response.write(AddPage_HTML)
		self.response.headers['Content-Type'] = 'text/html'
	
class Add(webapp2.RequestHandler):
	def post(self):
		uuu = users.get_current_user()
		name = uuu.nickname()
		publish_year = self.request.get("publish_year")
		source = self.request.get("source")
		title = self.request.get("title")
		new_paper = Paper(name=name,publish_year=publish_year,title=title,source=source)
		new_paper_key = new_paper.put()
		upload_url = blobstore.create_upload_url('/upload/upload')
		self.response.write(Add_HTML % upload_url)
		self.response.headers['Content-Type'] = 'text/html'

app = webapp2.WSGIApplication([
	('/Add/AddPage',AddPage),
	('/Add/add',Add),
], debug=True)
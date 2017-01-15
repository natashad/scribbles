from django.db import models

class Paste(models.Model):
	content = models.TextField()
	pub_date = models.DateTimeField('date published')
	is_private = models.BooleanField(default=True)
	token = models.CharField(max_length=40, primary_key=True)
	password = models.CharField(max_length=60, default='')

	def __str__(self):
		return self.token + ": " + self.content
from django.db import models
# Create your models here.


class Functions:
	@staticmethod
	def get_message(request_method):
		return {key: value for key, value in request_method.items()}


class Comment(models.Model):
	'all comments in Person'
	# service info
	id = models.AutoField(editable=False, primary_key=True)
	made_for = models.ForeignKey(to='Person', on_delete=models.PROTECT)
	# body
	comm_date = models.DateField(auto_now=True)
	comment = models.TextField()
	attrs = ['id', 'made_for', 'comm_date', 'comment']


class Person(models.Model):
	'физические лица'
	# service info
	id = models.AutoField(editable=False, primary_key=True)
	# person info
	name = models.CharField(max_length=20)
	patronymic = models.CharField(max_length=20, blank=True)
	surname = models.CharField(max_length=20)
	# contacts
	first_phone_number = models.CharField(max_length=11, blank=True)
	second_phone_number = models.CharField(max_length=11, blank=True)
	first_email = models.EmailField(blank=True)
	second_email = models.EmailField(blank=True)
	# work data
	simple_comment = models.TextField(blank=True)
	attrs = ['id', 'name', 'patronymic', 'surname',
			'first_phone_number', 'second_phone_number', 'first_email', 
			'second_email', 'simple_comment']

	def __str__(self):
		full_name = f'{self.id}:{self.surname} {self.name} {self.patronymic}'
		return full_name

	def get_attrs_values(self):
		dictionary = {}
		for attr in self.attrs:
			try: dictionary[attr.__str__()] = eval('self.'+attr)
			except Exception: continue
		return dictionary

	def set_attrs(self, post_attrs):
		for attr in post_attrs:
			if attr in self.attrs:
				exec('self.'+attr+'=post_attrs[attr]')
		return self

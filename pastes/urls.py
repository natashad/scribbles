from django.conf.urls import url

from . import views

app_name='pastes'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^save$', views.save, name='save'),
	url(r'^show/(.*)$', views.show, name='show'),
]
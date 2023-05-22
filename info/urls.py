from django.urls import re_path
# from info.filter import SkillFilter
from info.forms import LoginForm
from info.views import *
from django.contrib.auth import views

worker_url = [
    re_path(r'^skill/create/$', SkillCreate.as_view(), name='createskill'),
    re_path(r'^skill/$', SkillListView.as_view(), name='skilllist'),
    re_path(r'^skill/delete/(?P<pk>\d+)/$', DeleteSkillView.as_view(), name='skilldelete'),
    re_path(r'^skill/update/(?P<pk>\d+)/$', SkillUpdate.as_view(), name='skillupdate'),
    re_path(r'^workerprofile/$', CreateProfile.as_view(), name='workerprofile'),
]

urlpatterns = [
    re_path(r'^$', home, name='home'),
    re_path(r'^registeration/', register, name='register'),
    re_path(
        r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    re_path(r'^login/', loginuser, name='login'),
    re_path(r'^profile/$', GetProfile.as_view(), name='profile'),
    re_path(r'^contractorprofile/$', CreateContractorProfile.as_view(), name='contractorprofile'),
    re_path(r'^aboutus/', aboutus, name='aboutus'),
    re_path(r'^contactus/', contactus, name='contactus'),
    re_path(r'^logout/$', views.LogoutView.as_view(), {'next_page': '/login'}, name='logout'),
    re_path(r'^worker-hire/$', WorkerSkillListView.as_view(), name='worker_skill_list'),
    re_path(r'^worker-hire/(?P<pk>\d+)/$', HireWorkerView.as_view(), name='worker_hire'),
    re_path(r'^hired-request/', HireRequestList.as_view(), name='hired_request'),
    re_path(r'^confirm-hire/(?P<pk>\d+)/$', confirm_hire_worker, name='confirm-hire'),
] + worker_url
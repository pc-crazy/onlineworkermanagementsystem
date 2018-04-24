from django.conf.urls import url

from info.filter import SkillFilter
from info.forms import LoginForm
from info.views import *
from django.contrib.auth import views

worker_url = [
    url(r'skill/create/$',SkillCreate.as_view(),name='createskill'),
    url(r'skill/$',SkillListView.as_view(),name='skillliist'),
    url(r'skill/delete/(?P<pk>\d+)/$',DeleteSkillView.as_view(),name='skilldelete'),
    url(r'skill/update/(?P<pk>\d+)/$',SkillUpdate.as_view(),name='skillupdate'),
    url(r'^workerprofile/$', CreateProfile.as_view(), name='workerprofile'),
]


urlpatterns = [

    url(r'^$', home, name='home'),
    url(r'^registeration/', register, name='register'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    url(r'^login/',loginuser, name='login'),
    url(r'^profile/$', GetProfile.as_view(),name =  'profile' ),
    url(r'^contractorprofile/$', CreateContractorProfile.as_view(), name='contractorprofile'),
    url(r'^aboutus/',aboutus, name='aboutus'),
    url(r'^contactus/',contactus, name='contactus'),
    url(r'^logout/$',views.logout, {'next_page': '/login'},name='logout'),
    url(r'worker-hire/$',WorkerSkillListView.as_view(),name='worker_skill_list'),
    url(r'^worker-hire/(?P<pk>\d+)/$',HireWorkerView.as_view(),name='worker_hire'),
    url(r'^hired-request/', HireRequestList.as_view(),name='hired_request'),
    url(r'^confirm-hire/(?P<pk>\d+)/$',confirm_hire_worker, name='confirm-hire'),


] + worker_url
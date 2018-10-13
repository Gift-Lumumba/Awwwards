from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    url('^$',views.index,name = 'index'),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'^project/$', views.upload_project, name='upload_project'),
    url(r'^user/(\d+)$', views.profile, name='profile'),
    url(r'^update/',views.update_profile,name='update_profile'),
    url(r'^api/projects/$', views.ProjectList.as_view()),
    url(r'api/projects/project-id/(?P<pk>[0-9]+)/$',
    views.ProjectDescription.as_view()),
    url(r'^api/profiles/$', views.ProfileList.as_view()),
    url(r'api/profiles/profile-id/(?P<pk>[0-9]+)/$',
    views.ProfileDescription.as_view())
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
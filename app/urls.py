from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    url('^$',views.index,name = 'index'),
    # url(r'^signup/$', views.signup, name='signup'),
    # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     views.activate, name='activate'),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'^project/$', views.upload_project, name='upload_project'),
    url(r'^user/(\d+)$', views.profile, name='profile'),
    url(r'^profile/update/$', views.update_profile, name='update_profile'),
    url(r'^api/projects/$', views.ProjectList.as_view()),
    url(r'api/projects/project-id/(?P<pk>[0-9]+)/$',
    views.ProjectDescription.as_view()),
    url(r'^api/profiles/$', views.ProfileList.as_view()),
    url(r'api/profiles/profile-id/(?P<pk>[0-9]+)/$',
    views.ProfileDescription.as_view()),
    url(r'^post/(?P<project_id>[0-9]+)/review_design/$', views.add_design, name='add_design'),
    url(r'^post/(?P<project_id>[0-9]+)/review_usability/$', views.add_usability, name='review_usability'),
    url(r'^post/(?P<project_id>[0-9]+)/review_content/$', views.add_content, name='review_content'),

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
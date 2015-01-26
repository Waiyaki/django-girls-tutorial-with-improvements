from django.conf.urls import patterns, include, url
from django.contrib import admin

from registration.backends.simple.views import RegistrationView


# New class that redirect the user to the main page if login successful.
class MyRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        return '/blog/'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    url(r'', include('blog.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name="registration_register"),
    url(r'^accounts/', include('registration.backends.simple.urls')),
)

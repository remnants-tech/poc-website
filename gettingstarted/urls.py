from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import christ_connects_app.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', christ_connects_app.views.index, name='index'),
    #url(r'^db', hello.views.db, name='db'),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^log-in', christ_connects_app.views.log_in, name='log-in'),
    url(r'^sign_up',christ_connects_app.views.sign_up, name='sign_up'),
    url(r'^pull_churches',christ_connects_app.views.pull_churches, name='pull_churches')
]


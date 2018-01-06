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
    url(r'^log_in', christ_connects_app.views.log_in, name='log_in'),
    url(r'^sign_up',christ_connects_app.views.sign_up, name='sign_up'),
    url(r'^user_sign_up',christ_connects_app.views.user_sign_up, name='user_sign_up'),
    url(r'^pull_churches',christ_connects_app.views.pull_churches, name='pull_churches'),
    url(r'^account_confirm',christ_connects_app.views.account_confirm, name='account_confirm')
]


from django.conf.urls import url

urlpatterns = [
    url(r'^(?P<path>.*)/$', 'django_contract.views.serve', name='serve'),
]

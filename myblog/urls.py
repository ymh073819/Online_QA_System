from django.conf.urls import include,url

from django.contrib import admin
admin.autodiscover()
from myblog.views import *
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [                         #r'XXXX'表示''内部的字符串默认不转义
    # Examples:
    # url(r'^$', 'myblog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^login/$', alogin),
    url(r'^register/login$', alogin),
    url(r'^register/$', register),
    url(r'^logout/view_all$',bg),
    url(r'^logout/$', alogout),
    url(r'^admin/', admin.site.urls),
    url(r'^post/$',post),
    url(r'^$',bg),
    url(r'^poll/$',get_poll_article),
    url(r'^deletepoll/$',delete_poll_article),
    url(r'^view_all/$',view_all),
    #url(r'^login/view_all$',view_all),
    url(r'^article/$',article),
    url(r'^answer/$',answer),
    url(r'^hot/$',hot),
    url(r'^new_msg/$',new_msg),
    url(r'^view_all_attention/$',view_all_attention),
    url(r'^article_attention/$',article_attention),
    url(r'^cancel_view_all_attention/$',cancel_view_all_attention),
    url(r'^personal_inf/$',personal_inf),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


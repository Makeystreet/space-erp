from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'space.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),


    #Space main page
    url(r'^$', 'erp.views.space_page', name='space_home'),
    url(r'^members/', 'erp.views.space_members_page', name='space_members'),
    url(r'^inventory/', 'erp.views.space_inventory_page', name='space_inventory'),

)

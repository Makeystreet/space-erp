from django.conf.urls import patterns, include, url
from tastypie.api import Api

from api import *

v1_api = Api(api_name='v1')

v1_api.register(UserResource())

# Space Page
v1_api.register(SpaceResource())
v1_api.register(PartResource())
v1_api.register(InventoryResource())


urlpatterns = patterns('',
                       url(r'', include(v1_api.urls)),
                       )

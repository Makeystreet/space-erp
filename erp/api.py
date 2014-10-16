from datetime import datetime

from django.conf.urls import url
from django.contrib.auth.models import User

from tastypie import fields
from tastypie.authorization import Authorization, ReadOnlyAuthorization
from tastypie.exceptions import Unauthorized
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpForbidden
from tastypie.resources import ModelResource
from tastypie.throttle import BaseThrottle
from tastypie.utils import trailing_slash

# from allauth.socialaccount.models import SocialAccount

from models import *

import unicodedata
import operator
import string

from urllib2 import urlopen, Request
import json
import re

from django.db.models import Count
from django.db.models import Q


# slight variation to the default model resource
class DefaultModelResource(ModelResource):
    def hydrate_added_time(self, bundle):
        if bundle.data['added_time'] == "Now" or\
                bundle.data['added_time'] == "":
            bundle.data["added_time"] = datetime.now()
        return bundle

    def hydrate_user(self, bundle):
        if bundle.request.method == "POST":
            bundle.data["user"] = bundle.request.user
        return bundle

    def obj_delete_list(self, bundle, **kwargs):
        raise ImmediateHttpResponse(
            HttpForbidden("You do not have the required permissions"))


# This is a class that created by Alex - for all common meta settings.
class DefaultMeta:
    authorization = Authorization()
    always_return_data = True
    include_resource_uri = True


class UserResource(DefaultModelResource):
    # instructables.

    class Meta:
        queryset = User.objects.all()
        resources = "user"
        fields = ['id', 'username', 'first_name', 'last_name', 'last_login',
                  'first_name', 'last_name', 'date_joined',
                  'email']
        authorization = Authorization()
        allowed_methods = ['get']
        filtering = {
            'date_joined': ('lte', 'gte'),
            'last_login': ('lte', 'gte'),
        }


    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_search'),
                name="api_get_search"),
        ]


    def get_search(self, request, **kwargs):
        q = request.GET.get('q', '')
        if q:
            users = User.objects\
                .filter(is_active=True)\
                .filter(Q(first_name__icontains=q) |
                        Q(last_name__icontains=q))[:10]

            results = []
            for user in users:
                bundle = self.build_bundle(obj=user, request=request)
                bundle = self.full_dehydrate(bundle)
                results.append(bundle)
            results_list = {
                'users': results,
            }
            return self.create_response(request, results_list)



class PartResource(DefaultModelResource):
    user = fields.ForeignKey(UserResource, 'user', null=True, blank=True,
                             full=True)

    class Meta(DefaultMeta):
        queryset = Part.objects.all()
        resource_name = "part"
        authorization = Authorization()

class SpaceResource(DefaultModelResource):
    members = fields.ManyToManyField(UserResource, 'members', null=True,
                                     blank=True, full=True)

    class Meta(DefaultMeta):
        queryset = Space.objects.all().order_by('id').reverse().\
            filter(is_enabled=True)
        resource_name = 'space'
        authorization = Authorization()
        include_resource_uri = False
        always_return_data = True


    def hydrate_members(self, bundle):
        if len(bundle.data['members']) > 0 and\
                type(bundle.data['members'][0]) is not unicode:
            return bundle

        space = Space.objects.get(id=int(bundle.data['id']))

        new_list = bundle.data['members']
        admin_list = ['/api/v1/user/' + str(user.id) + '/'
                      for user in space.admins.all()]
        non_admin_list = [x for x in new_list if x not in admin_list]

        final_list = admin_list + non_admin_list
        bundle.data['members'] = final_list
        return bundle

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_search'), name="api_get_search"),
        ]

    def get_search(self, request, **kwargs):
        q = request.GET.get('q', '')
        if q:
            spaces = Space.objects\
                .filter(Q(name__icontains=q))[:10]

            results = []
            for space in spaces:
                bundle = self.build_bundle(obj=space, request=request)
                bundle = self.full_dehydrate(bundle)
                results.append(bundle)
            results_list = {
                'spaces': results,
            }
            return self.create_response(request, results_list)


class InventoryResource(DefaultModelResource):
    part = fields.ForeignKey(PartResource, 'part', full=True)
    space = fields.ForeignKey(SpaceResource, 'space')
    quantity = fields.IntegerField(attribute='quantity')
    owner = fields.CharField(attribute='owner', null=True, blank=True)

    class Meta(DefaultMeta):
        queryset = Inventory.objects.order_by('?')
        resource_name = "inventory"
        authorization = Authorization()
        filtering = {
            'part': 'exact',
            'space': 'exact',
        }


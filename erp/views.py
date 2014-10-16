import json

from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect

from models import Space, Inventory
from forms import LoginForm


def get_user_details_json(request):
    login = request.user.is_authenticated()

    user_details = {}
    if login:
        cur_user = User.objects.get(username=request.user.username)
        user_details["id"] = cur_user.id
        user_details = json.dumps(user_details)
    else:
        user_details = {}

    return user_details


def space_page(request):
    user_details = get_user_details_json(request)
    space = Space.objects.get(pk=1)
    is_space_admin = False

    if space:
        space.no_admins = space.admins.count()
        space.no_members = space.members.count()
        space.inventory_list = Inventory.objects.filter(space=1)

        if request.user in space.admins.all():
            is_space_admin = True

        return render(request, 'space_page.html', {
            'space': space,
            'user_details': user_details,
            'is_space_admin': is_space_admin,
        })
    else:
        return HttpResponse('404 - Space not configured')


def space_members_page(request):
    user_details = get_user_details_json(request)

    space = Space.objects.get(pk=1)
    is_space_admin = False
    if space:
        space.no_admins = space.admins.count()
        space.no_members = space.members.count()
        space.inventory_list = Inventory.objects.filter(space=1)

        if request.user in space.admins.all():
            is_space_admin = True

        return render(request, 'space_members_page.html', {
            'space': space,
            'user_details': user_details,
            'is_space_admin': is_space_admin,
        })
    else:
        return HttpResponse('404 - Space not configured')


def space_inventory_page(request):
    user_details = get_user_details_json(request)

    space = Space.objects.get(pk=1)
    is_space_admin = False
    if space:
        space.no_admins = space.admins.count()
        space.no_members = space.members.count()
        space.inventory_list = Inventory.objects.filter(space=1)

        if request.user in space.admins.all():
            is_space_admin = True

        return render(request, 'space_inventory_page.html', {
            'space': space,
            'user_details': user_details,
            'is_space_admin': is_space_admin,
        })
    else:
        return HttpResponse('404 - Space not configured')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('space_inventory'))
            else:
                messages.error(request, 'Login Failed! Please try again.')
        else:
            messages.error(request, 'Please check the details entered!')
    return render(request, 'login.html')

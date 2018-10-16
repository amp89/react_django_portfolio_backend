from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
# Create your views here.
from rest_framework import authentication, permissions
from django.views import View
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import *

class GetUserViewMixin(View):
    def dispatch(self,request,*args,**kwargs):
        if request.user.is_anonymous and request.META.get("HTTP_AUTHORIZATION"):
            the_key = request.META.get("HTTP_AUTHORIZATION").split(" ")[-1]
            print("..................")
            print(the_key)
            self.token_user = Token.objects.get(key=the_key).user
            print(f"the token user iiiiiissss {self.token_user}")
        elif not request.user.is_anonymous and request.user:
            print(f"the normal user is.... {request.user}")
            self.token_user = request.user
        else:
            self.token_user = None
        return super(GetUserViewMixin,self).dispatch(request,*args,**kwargs)


class GetUserAPIViewMixin(APIView):
    def dispatch(self,request,*args,**kwargs):
        if request.user.is_anonymous and request.META.get("HTTP_AUTHORIZATION"):
            the_key = request.META.get("HTTP_AUTHORIZATION").split(" ")[-1]
            print("..................")
            print(the_key)
            self.token_user = Token.objects.get(key=the_key).user
            print(f"the token user iiiiiissss {self.token_user}")
        elif not request.user.is_anonymous and request.user:
            self.token_user = request.user
        else:
            self.token_user = None
        return super(GetUserViewMixin,self).dispatch(request,*args,**kwargs)




class ContactInfoView(GetUserViewMixin):
    authentication_classes = (authentication.TokenAuthentication,)
    def get(self,request):
        print(request.META)
        print(self.token_user)

        contact_info_object = ContactInfo.load()
        contact_info_dict = {
            "github":contact_info_object.github,
            "linkedin":contact_info_object.linkedin,
            "blog":contact_info_object.blog,
            "email":None,
            "phone":None
        }

        if self.token_user:
            contact_info_dict["email"] = contact_info_object.email
            contact_info_dict["phone"] = contact_info_object.phone

        return JsonResponse(contact_info_dict)

class SiteInfoView(View):
    def get(self,request):
        site_info_object = SiteInfo.load()
        response_dict = {
            "photo_1_link":site_info_object.photo_1_link,
            "photo_2_link":site_info_object.photo_2_link,
            "photo_3_link":site_info_object.photo_3_link,
            "about":site_info_object.about
        }
        return JsonResponse(response_dict)

class ProjectView(View):
    def get(self,request):
        project_dict = list(Project.objects.select_related().all().order_by("-datetime").values())
        return JsonResponse(project_dict,safe=False)


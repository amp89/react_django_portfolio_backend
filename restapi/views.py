from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
# Create your views here.
from rest_framework import authentication, permissions
from django.views import View
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import *
from django.contrib.auth.models import User
import json
from django.conf import settings

class GetUserViewMixin(View):
    def dispatch(self,request,*args,**kwargs):
        print(request.META)
        print(request.body)
        print(request.GET)
        print(request.POST)
        print(request.COOKIES)
        print(dir(request.META))
        print(dir(request))
        print("reqmeth: ", request.method)
        if request.user.is_anonymous and request.META.get("HTTP_AUTHORIZATION"):
            the_key = request.META.get("HTTP_AUTHORIZATION").split(" ")[-1]
            the_other_key = request.META.get("HTTP_AUTHORIZATION").split(" ")[-1]
            print(f"..................the key ...................... {the_key}")
            print(f"..................the .. other ... key ...................... {the_other_key}")
            print(the_key)
            try:
                self.token_user = Token.objects.get(key=the_key).user
            except:
                self.token_user = None
            print(f"the token user iiiiiissss {self.token_user}")
        elif not request.user.is_anonymous and request.user:
            print(f"the normal user is.... {request.user}")
            self.token_user = request.user
        else:
            print("user not found")
            self.token_user = None
        return super(GetUserViewMixin,self).dispatch(request,*args,**kwargs)


# class GetUserAPIViewMixin(APIView):
#     def dispatch(self,request,*args,**kwargs):
#         if request.user.is_anonymous and request.META.get("HTTP_AUTHORIZATION"):
#             the_key = request.META.get("HTTP_AUTHORIZATION").split(" ")[-1]
#             print("..................")
#             print(the_key)
#             self.token_user = Token.objects.get(key=the_key).user
#             print(f"the token user iiiiiissss {self.token_user}")
#         elif not request.user.is_anonymous and request.user:
#             self.token_user = request.user
#         else:
#             self.token_user = None
#         return super(GetUserViewMixin,self).dispatch(request,*args,**kwargs)




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

class SiteInfoView(GetUserViewMixin):
    def get(self,request):
        site_info_object = SiteInfo.load()
        site_title = settings.SITE_TITLE
        site_author = settings.SITE_AUTHOR
        response_dict = {
            "photo_1_link":site_info_object.photo_1_link,
            "photo_2_link":site_info_object.photo_2_link,
            "photo_3_link":site_info_object.photo_3_link,
            "about":site_info_object.about,
            "site_title":site_title,

            "site_author":site_author,
        }
        if self.token_user:
            response_dict["at"] = self.token_user.token.key
        return JsonResponse(response_dict)

class ProjectView(View):
    def get(self,request):
        project_dict = list(Project.objects.select_related().all().order_by("-datetime").values())
        return JsonResponse(project_dict,safe=False)


class Login(View):
    def post(self,request):
        print(request.body)
        username = json.loads(request.body.decode("utf-8")).get("usr")
        password = json.loads(request.body.decode("utf-8")).get("pwd")
        print(f"asldfjlasdkfj {username}")
        user_obj = User.objects.get(username=username)
        if user_obj.check_password(password):
            return JsonResponse({
                    "at":Token.objects.get_or_create(user=user_obj)[0].key,
                    "username":user_obj.username,
                    "firstname":user_obj.first_name,
                    "lastname":user_obj.last_name,
                    "loggedIn":True,
                    "result":[]
                })
        else:
            return JsonResponse({
                    "at":None,
                    "username":None,
                    "firstname":None,
                    "lastname":None,
                    "loggedIn":False,
                    "result":["Login Failed",]
                }, safe=False)

class Logout(GetUserViewMixin):
    def options(self,request):
        print("optoin")
        response = JsonResponse({"wtf":"ok"})
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        return response

    def get(self,request):
        print("logout get: {}".format(request.method))
        if self.token_user:
            t = Token.objects.get(user=self.token_user)
            t.delete()
            response =  JsonResponse({
                    "at":None,
                    "username":None,
                    "firstname":None,
                    "lastname":None,
                    "loggedIn":False,
                })
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
            response["Access-Control-Max-Age"] = "1000"
            response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
            print("logging out?")
            return response
        else:
            response = JsonResponse({
                    "at":None,
                    "username":None,
                    "firstname":None,
                    "lastname":None,
                    "loggedIn":False,
                })
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
            response["Access-Control-Max-Age"] = "1000"
            response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
            print("not logging out?")
            return response

class MessageView(GetUserViewMixin):
    def post(self,request):
        request_dict = json.loads(request.body.decode("utf-8"))
        subject = request_dict.get("subject")
        message_body = request_dict.get("body")
        if self.token_user:
            message_obj = Message(
                user=self.token_user,
                subject=subject,
                body=message_body
            )
            message_obj.save()
            return JsonResponse({"result":["Message Sent"],"done":True})
        else:
            return JsonResponse({"result":["Please Login and Try Agin"],"done":False})

class SignupView(View):
    def post(self, request):
        request_dict = json.loads(request.body.decode("utf-8"))
        first_name = request_dict["firstname"]
        last_name = request_dict["lastname"]
        email = request_dict["email"]
        p = request_dict["pwd1"]
        p2 = request_dict["pwd2"]
        errs = []
        if p != p2 or len(p) < 8:
            errs.append("Passwords much match and be over 8 characters")
        if not first_name:
            errs.append("First name is required")
        if not last_name:
            errs.append("Last name is requred")
        if not email:
            errs.append("Email is required")
        if errs:
            return JsonResponse({"result":errs}, safe=False)
        else:
            u, created = User.objects.get_or_create(
                username=email,
                email = email,
                first_name=first_name,
                last_name=last_name,
            )
            
            if created:
                u.set_password(p)
                return JsonResponse({"result": [f"Thanks, {first_name}! Please login."]}, safe=False)
            else:
                return JsonResponse({"result": [f"That email has been taken!"]}, safe=False)
            
            
        
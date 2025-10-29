from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view
# from django.db import IntegrityError
from  django.contrib.auth import authenticate,login
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from .models import *
from .serializers import * 
import logging

# 
# from rest_framework.exceptions import ValidationError
# from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.tokens import RefreshToken,AuthUser


from django.utils import timezone
from  rest_framework import status

# Create your views here.

logger = logging.getLogger(__name__)


def get_tokens_for_user(user):
   refresh=RefreshToken.for_user(user) 
   return {
      'refresh':str(refresh),
      'access':str(refresh.access_token)
     }


@api_view(['POST'])
def register(request):
   try:
     logger.info("start order to register")
     passw=request.data.get('password')
     age=request.data.get('age')
     user_name=request.data.get('user_name')
     school=request.data.get('school')
     first_name=request.data.get('first_name')
     last_name=request.data.get('last_name')
     if len(passw)<8 :
        logger.warning('you should add password with 8 character')
        raise ValueError("you must add a password with 8 character or more..")
     if type(age) is not int:
          logger.warning('you should add numeric variable')
          raise ValueError("you should add numeric variable")
     if  int (age)  < 9  or  int (age) > 90 :
          logger.warning('your age must be betwen 9 and 90')
          raise ValueError("your age must be betwen 9 and 90")
     if  User.objects.filter(username=user_name).exists():
          logger.error('this email is already exist')
          raise ValueError("this email is already exist")
     user=User.objects.create_user(username=user_name,password=passw,first_name=first_name,last_name=last_name)
     token=get_tokens_for_user(user)
     us=profile(user=user,age=age,school=school,token=token['access']
     )
     us.save()
     logger.info("the user create successfully")
     return Response({"result":"ok","token":us.token})
   except Exception as e:
      print(e)
      logger.error(f'something happend {e}')
      raise ValueError(f"Error : {e}")
   





@api_view(['POST'])
def Login(request):
   try:
     passw=request.data.get('password')
     user_name=request.data.get('user_name')
     user=authenticate(username=user_name,password=passw)
     token=get_tokens_for_user(user)
     prof=profile.objects.get(user=user)
     prof.token=token['access']
     prof.save()
     return Response({"result":"ok","token":prof.token})
   except Exception as e:
      print(e)
      return Response({"result" : "error"})    
   




@api_view(['POST'])
def get_profile(request):
   try:
    token=request.data.get('token')
    prof=profile.objects.get(token=token)
    details=Profileserializer(prof)
    return Response({"result":"ok","details":details.data})
   except Exception as e:
      print(e)
      return Response({"result" : "error"})   





@api_view(['GET'])
def read_posts(request):
   try:
    allposts=post.objects.all()
    serializerposts = PostSerializer(allposts, many=True)
  
    return Response({"result":"ok","data":serializerposts.data})
   except Exception as e:
      print(e)
      return Response({"result" : "error"}) 
   



@api_view(['POST'])
def create_post(request):
   try:
    token=request.data.get('token')
    text=request.data.get('text')
    image=request.FILES.get('image')
    print('hello')
    prof=profile.objects.get(token=token)
  
    post_for_user=post(u=prof,text=text)
    post_for_user.save()
    post_for_user.image=image
    post_for_user.save()
    return Response({"result":"ok","id":post_for_user.id})
   except Exception as e:
      print(e)
      return Response({"result" : "error"})    
   




@api_view(['POST'])
def update_post(request):
   try:
    id=request.data.get('id')
    text=request.data.get('text')
    image=request.FILES.get('image')
    print('hello')
    post_for_user=post.objects.get(id=id)
    post_for_user.text=text
    post_for_user.image=image
    post_for_user.save()
    return Response({"result":"ok"})
   except Exception as e:
      print(e)
      return Response({"result" : "error"})    
   




@api_view(['POST'])
def delet_post(request):
   try:
    id=request.data.get('id')
    post_for_user=post.objects.get(id=id)
    post_for_user.delete()
    
 
    return Response({"result":"ok"})
   except Exception as e:
      print(e)
      return Response({"result" : "error"})     
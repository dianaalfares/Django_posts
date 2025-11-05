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
      # logger.error(f'something happend {e}')
      raise ValueError(f"Error :{e}")
   





@api_view(['POST'])
def Login(request):
   try:
     logger.info("start order to log in")
     passw=request.data.get('password')
     user_name=request.data.get('user_name')
     if len(passw)<8 :
        logger.warning('you should add password with 8 character or more..')
        raise ValueError("you must add a password with 8 character or more..")
     if  not  User.objects.filter(username=user_name):
        logger.error('user name doesnot exist')
        raise ValueError("user name doesnot exist")
     user=authenticate(username=user_name,password=passw)
     if not user :
       logger.error('wrong password')
       raise ValueError("wrong password")
     token=get_tokens_for_user(user)
     prof=profile.objects.get(user=user)
     prof.token=token['access']
     prof.save()
     logger.info('Log in is ok')
     return Response({"result":"ok","token":prof.token})
   except Exception as e:
      raise ValueError(f"Error : {e}") 
   




@api_view(['POST'])
def get_profile(request):
   try:
    logger.info("start order to get profile")
    token=request.data.get('token')
    prof=profile.objects.get(token=token)
    details=Profileserializer(prof)
    logger.info("all data are prepeared")
    return Response({"result":"ok","details":details.data})
   except Exception as e:
       raise ValueError(f"Error :{e}")  





@api_view(['GET'])
def read_posts(request):
   try:
    logger.info("start order to read all posts")
    allposts=post.objects.all()
    serializerposts = PostSerializer(allposts, many=True)
    logger.info("every thing ok")
    return Response({"result":"ok","data":serializerposts.data})
   except Exception as e:
     raise ValueError(f"Error :{e}")   
   



@api_view(['POST'])
def create_post(request):
   try:
    logger.info("start order to create post")
    token=request.data.get('token')
    text=request.data.get('text')
    image=request.FILES.get('image')
    prof=profile.objects.get(token=token)
    post_for_user=post(u=prof,text=text,image=image)
    post_for_user.save()
    logger.info("every thing ok")
    return Response({"result":"ok","id":post_for_user.id})
   except Exception as e:
    raise ValueError(f"Error :{e}")       
   




@api_view(['PUT'])
def update_post(request):
   try:
    logger.info("start order to update post")
    id=request.data.get('id')
    token=request.data.get('token')
    text=request.data.get('text')
    image=request.FILES.get('image')
    if  not profile.objects.get(token=token):
       logger.error("token is not correct")
       raise ValueError("token is not correct") 
    if  not post.objects.get(id=id):
       logger.error("id does not correct")
       raise ValueError("id does not correct") 
    prof=profile.objects.get(token =token)
    if  not post.objects.filter(u=prof,id=id):
       logger.error("post does not belong to this user")
       raise ValueError("post does not belong to this user") 
    post_for_user=post.objects.get(id=id)
    post_for_user.text=text
    post_for_user.image=image
    post_for_user.save()
    logger.info("every thing ok")
    return Response({"result":"ok"})
   except Exception as e:
     raise ValueError(f"Error :{e}")       
       
   




@api_view(['DELETE'])
def delet_post(request):
   try:
    logger.info("start order to delete post")
    id=request.data.get('id')
    token=request.data.get('token')
    if  not profile.objects.get(token=token):
       logger.error("token is not correct")
       raise ValueError("token is not correct") 
    if  not post.objects.get(id=id):
       logger.error("id does not correct")
       raise ValueError("id does not correct") 
    prof=profile.objects.get(token =token)
    if  not post.objects.filter(u=prof,id=id):
       logger.error("post does not belong to this user")
       raise ValueError("post does not belong to this user") 

    post_for_user=post.objects.get(id=id)
    post_for_user.delete()
    
    logger.info("every thing ok")
    return Response({"result":"ok"})
   except Exception as e:
     raise ValueError(f"Error :{e}")    
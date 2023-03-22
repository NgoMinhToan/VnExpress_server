import time
from datetime import datetime
from django.shortcuts import render
from dateutil import tz
import re
# Create your views here.

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

# from models import News
from vnexpressAPI.models import News, NewsCategory, detail_news
from vnexpressAPI.serializers import DetailNewsSerializer, NewsSerializer, NewsCategorySerializer

from vnexpressAPI.methods import refresh_top_news, delete_all_news, update_news, to_url_param

from bson import ObjectId

class ListCreateNewsView(ListCreateAPIView):
    model = News
    serializer_class = NewsSerializer
    queryset = News.objects.all()

# class UpdateDeleteNewsView(RetrieveUpdateDestroyAPIView):
#     model = News
#     serializer_class = DetailNewsSerializer
#     queryset = News.objects.all()

#     def put(self, request, *args, **kwargs):
#         news = get_object_or_404(News, id=kwargs.get('pk'))
#         serializer = DetailNewsSerializer(news, data=request.data)

#         if serializer.is_valid():
#             serializer.save()

#             return JsonResponse({
#                 'message': 'Update News successful!'
#             }, status=status.HTTP_200_OK)

#         return JsonResponse({
#             'message': 'Update News unsuccessful!'
#         }, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, *args, **kwargs):
#         news = get_object_or_404(News, id=kwargs.get('pk'))
#         news.delete()

#         return JsonResponse({
#             'message': 'Delete News successful!'
#         }, status=status.HTTP_200_OK)


def init_news_api(request):   
    refresh_top_news()
    
    return JsonResponse({
        'message': 'Refresh top news successful!'
    }, status=status.HTTP_200_OK)

def cron(request):
    host = request.headers.get('Host')
    return JHttpResponseRedirect(redirect_to=host + '/update_news')
    # sonResponse({
    #     'message': 'News have been update!'
    # }, status=status.HTTP_200_OK)
    

def update_news_api(request):
    update_news()
    return JsonResponse({
        'message': 'News have been update!'
    }, status=status.HTTP_200_OK)

def delete_news_api(request):
    try:
        delete_all_news()
    except News.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Fail to delete news!'
        }, status=status.HTTP_200_OK)
    return JsonResponse({
        'success': True,
        'message':'All news have been delete!'
    }, status=status.HTTP_200_OK)

def getListNews(request, from_, to):
    all_news = News.objects.all().order_by('-datetime')[from_:to]
    serializer = NewsSerializer(all_news, many=True)
    return JsonResponse(serializer.data, safe=False)

def getNews(request, news_url_param):
    try:
        news = News.objects.get(news_url_param=news_url_param)
    except News.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'News not found!'
        }, status=status.HTTP_200_OK)
    serializer = DetailNewsSerializer(news)
    return JsonResponse({
        'success': True,
        'message':'Founded!',
        'data': serializer.data
    }, status=status.HTTP_200_OK)

def get_category(request):
    all_category = NewsCategory.objects.all()
    serializer = NewsCategorySerializer(all_category, many=True)
    return JsonResponse(serializer.data, safe=False)

def get_category_news(request, name):
    param_name = to_url_param(name)
    all_news = News.objects.filter(category__param_name__contains=param_name).order_by('-datetime')
    serializer = NewsSerializer(all_news, many=True)
    return JsonResponse(serializer.data, safe=False)

def get_category_news_range(request, name, from_, to):
    param_name = to_url_param(name)
    all_news = News.objects.filter(category__param_name__contains=param_name).order_by('-datetime')[from_:to]
    serializer = NewsSerializer(all_news, many=True)
    return JsonResponse(serializer.data, safe=False)

def search_news(request, keyword):
    print('Search for keyword:', keyword)
    all_news = News.objects.filter(news_url_param__icontains=to_url_param(keyword)).order_by('-datetime')[:10]
    serializer = NewsSerializer(all_news, many=True)
    return JsonResponse(serializer.data, safe=False)
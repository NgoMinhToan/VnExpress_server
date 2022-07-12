from rest_framework import serializers
import json
from vnexpressAPI.models import News, detail_news, Media, NewsCategory

from vnexpressAPI.CustomField import ObjectIdField
from datetime import datetime

class MediaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'alt', 'src']

class DetailModelNewsSerializer(serializers.ModelSerializer):
    content = serializers.JSONField()
    media = MediaModelSerializer(many=True)
    class Meta:
        model = detail_news
        fields =  '__all__'
        
class NewsCategorySerializer(serializers.ModelSerializer):    
    class Meta:
        model = NewsCategory
        fields = '__all__'

 
class DetailNewsSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    detail = DetailModelNewsSerializer(read_only=True, many=False)
    category = NewsCategorySerializer(read_only=True, many=False)
    
    
    class Meta:
        model = News
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    category_param = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    news_type = serializers.SerializerMethodField()
    # datetime = serializers.SerializerMethodField()
    
    def get_category(self, obj):
        return obj.category.name
    
    def get_category_param(self, obj):
        return obj.category.param_name
    
    def get_description(self, obj):
        return obj.detail.description
    
    def get_news_type(self, obj):
        return obj.detail.news_type
    
    # def get_datetime(self, obj):
    #     return datetime.timestamp(obj.datetime)*1000
    
    class Meta: 
        model = News
        fields = ['id', 'category', 'category_param', 'news_type', 'title', 'description', 'news_url_param', 'datetime', 'link']       

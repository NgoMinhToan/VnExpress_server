from djongo import models
from django.db.models.query import QuerySet
from vnexpressAPI.crawl_data import crawl_news
import unidecode
import re

def to_url_param(text):
    return re.sub(r'\s+', '_', re.sub(r'\W+', ' ', unidecode.unidecode(text)).strip().lower())

# Create your models here.
class NewsQuerySet(QuerySet):
    def refresh_top_news(self):
        print('Delete all news!')
        self.all().delete()
        
        print('Crawl data!')
        all_news = crawl_news.crawl_top_express_news()
        
        print('Save data!')
        for news in all_news:
            n_ctgr = NewsCategory.objects.filter(name='_'.join(news['detail']['category']))
            if len(n_ctgr) == 0:
                n_ctgr = NewsCategory(name='_'.join(news['detail']['category']))
                n_ctgr.save()
            else:
                n_ctgr = n_ctgr.first()
            
            detail = news['detail']
            media_instance = [Media.objects.create(**i) for i in detail['media']]
            del detail['media'], detail['category']
            detail_instance = detail_news.objects.create(**detail)
            detail_instance.media.set(media_instance)
            news_item = self.create(
                title=news.get('title'),
                news_url_param=to_url_param(news.get('title')),
                datetime=news.get('datetime'),
                link=news.get('link'),
                category=n_ctgr,
                detail=detail_instance
            )

class NewsManager(models.Manager):
    def get_queryset(self):
        return NewsQuerySet(self.model, using=self._db)
    def __getattr__(self, attr, *args):
        # see https://code.djangoproject.com/ticket/15062 for details
        if attr.startswith("_"):
            raise AttributeError
        return getattr(self.get_queryset(), attr, *args)

class Media(models.Model):
    id = models.ObjectIdField(primary_key=True, db_column='_id')
    alt = models.CharField(max_length=255, blank=True, null=True)
    src = models.CharField(max_length=255, blank=True, null=True)
    detail_news = models.ForeignKey('detail_news', related_name='media', to_field='id', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.alt
    # class Meta:
        # app_label = 'mongodb'
        # abstract = True
        
class detail_news(models.Model):
    id = models.ObjectIdField(primary_key=True, db_column='_id')
    news_type = models.CharField(max_length=10, null=True)
    title = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=1000, null=True)
    content = models.JSONField(max_length=1000, null=True)
    author = models.CharField(max_length=50, null=True)
    raw_body = models.CharField(max_length=10000, null=True)
    # media = models.ArrayField(model_container=Media, blank=True, null=True)
    # news = models.OneToOneField('News', related_name='detail', on_delete=models.CASCADE, null=True)
    
    # def set_content(self, x):
    #     self.content = json.dumps(x)

    # class Meta:
        # app_label = 'mongodb'
        # abstract = True
    
    
    def __str__(self):
        return self.title

class NewsCategory(models.Model):
    id = models.ObjectIdField(primary_key=True, db_column='_id')
    name = models.CharField(max_length=50, null=True, unique=True)
    param_name = models.CharField(max_length=50, null=True, unique=True)
    
    
    def __str__(self):
        return self.name
    
    # class Meta:
        # app_label = 'mongodb'
    
class News(models.Model):
    id = models.ObjectIdField(primary_key=True, db_column='_id')
    title = models.CharField(max_length=200)
    news_url_param = models.CharField(max_length=200, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=200)
    category = models.ForeignKey('NewsCategory', related_name='news', to_field='id', on_delete=models.CASCADE, null=True)
    # detail = models.EmbeddedField(model_container=detail_news, blank=True, null=True)
    detail = models.OneToOneField('detail_news', related_name='news', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    objects = NewsManager()
    
    # class Meta:
        # app_label = 'mongodb'

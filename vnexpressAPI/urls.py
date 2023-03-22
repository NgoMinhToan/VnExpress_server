from django.urls import path
from vnexpressAPI import views
urlpatterns = [
    path('news/', views.ListCreateNewsView.as_view()),
    path('news/<int:from_>/<int:to>/', views.getListNews),
    # path('news/<str:pk>', views.UpdateDeleteNewsView.as_view()),
    path('init_news', views.init_news_api),
    path('cron', views.cron),
    path('update_news', views.update_news_api),
    path('delete_news', views.delete_news_api),
    path('getNews/<str:news_url_param>', views.getNews),
    path('get_category', views.get_category),
    path('get_category/<str:name>/', views.get_category_news),
    path('get_category/<str:name>/<int:from_>/<int:to>/', views.get_category_news_range),
    path('search/<str:keyword>', views.search_news),
    # path('')
]

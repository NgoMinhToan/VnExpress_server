# Setup environment
```python
vnE_news_env\Scripts\activate.bat
pip install -r requirements.txt

```
# Start the application
```python
!python manage.py makemigrations 
!python manage.py migrate 
!python manage.py runserver

```

# ENVIRONMENT
1. APP_SECRET_KEY: Random sercret key
2. DB_URI: mongo database URI
3. DB_NAME: mongo database name

```
APP_SECRET_KEY=django-insecure-2yv#y@u5hn!9yfjqxwbz((++2!(gcn&#_#b0+j2e@)ga96c#$3
DB_URI=mongodb+srv://[username:password@]host1[:port1][,...hostN[:portN]][/[defaultauthdb][?options]]
DB_NAME=VnExpress_Clone
```
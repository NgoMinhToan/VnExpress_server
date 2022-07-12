command: {
    start env: vnE_news_env\Scripts\activate.bat,
    import requirement: pip install -r requirements.txt
    start project:  !python manage.py makemigrations 
                    !python manage.py migrate 
                    !python manage.py runserver 8000
}
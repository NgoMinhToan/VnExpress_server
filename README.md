command: {
    start env: vnE_news_env\Scripts\activate.bat,
    import requirement: pip install -r requirements.txt
    start project:  !python manage.py makemigrations 
                    !python manage.py migrate 
<<<<<<< HEAD
                    !python manage.py runserver
}
=======
                    !python manage.py runserver 
}
>>>>>>> 2085af4538970cf58e9bbc3663a840dc857e0937

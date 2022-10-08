# youtube-search

## Setup
Docker way (only API Image)
1. docker-compose up

Non-Docker way

1. clone repository

2. create virtualenv of python(3.7.3) and activate it

3. pip install -r requirements.py

4. python manage.py migrate (to run existing migrations)

5. python manage.py createsuperuser (to access admin)

6. python manage.py collectstatic (static files for admin and swagger)

7. run celery and celery_beat to run the scheduler
   
   celery -A youtube_search worker
   
   celery -A youtube_search beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

8. schedule periodic task for youtube fetch data (http://localhost:8002/admin/django_celery_beat/periodictask/)

# API Endpoint

  chosen key_word : "corona"
  
  http://localhost:8002/search/?q=<search_string1>,<search_string2>
  
  http://localhost:8002/search/?q=<search_string1>


# Features of project:

1. Server calls the YouTube API continuously in background (async) with celery beat and as a add on we can configure scheduling by admin.

2. GET API with paginated response, advanced search keywords, and desc by upload time.

3. It's scalable and optimised, single api with admin panel with search, sort, filter (http://localhost:8002/admin/youtube_search/youtubevideo/)

4.  multiple API key support with refresh token method.

5. many more features related to admin, celery admin, advanced search results, scalable key word mapping in database, and many more.

from django.urls import path
from . import views
app_name = 'academics'
urlpatterns = [
    path('subjects/',views.manage_subject, name='manage_subjects')
]

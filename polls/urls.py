from django.urls import path,include

from . import views

from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [

    
    path('challenge/', views.ChallengeList.as_view()),
    path('challenge/<int:pk>/', views.ChallengeDetail.as_view()),
    path('join/', views.Join.as_view()),
    path('rank/', views.Rank.as_view()),
    path('check/', views.ChallengeCheck.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
from django.urls import path

from user import views

app_name = 'users'
urlpatterns = [
    path('', views.UserList.as_view()),
    path('<int:pk>/', views.UserInfo.as_view()),
    path('validate-email/<str:email>/', views.ValidateEmail.as_view()),
    path('pick-winner/', views.PickWinner.as_view())
]

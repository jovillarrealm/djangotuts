from django.urls import path 

from . import views 

 

urlpatterns = [ 

    path('todos/', views.TodoListCreate.as_view(), name='list'), 
    path('todos/<int:pk>', views.TodoRetrieveUpdateDestroy.as_view()), 
    path('todos/<int:pk>/complete', views.TodoToggleComplete.as_view()), 
    path('signup/', views.TodoToggleComplete.signup, name='signup'), 
    path('login/', views.TodoToggleComplete.login, name='login'), 
] 

 


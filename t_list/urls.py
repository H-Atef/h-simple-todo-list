
from . import views
from django.urls import path



urlpatterns = [
    path("update-list-status/<int:pk>/",views.update_list_status,name='update-list-status'),
    path('todos/', views.ToDoView.as_view(), name='todo-list'),
    path('todos/<int:pk>/', views.ToDoDetailView.as_view(), name='todo-detail'),
    path('todos-paginated-l/', views.get_paginated_todos_limit_offest, name='paginated-todos-l'),
    path('todos-paginated-p/', views.get_paginated_todos_page_num, name='paginated-todos-p'),
    path('todos-paginated/', views.get_paginated_todos, name='paginated-todos'),
]

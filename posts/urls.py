from django.urls import path
from .views import index, single_post, post_add, post_edit, post_delete, post_reaction, comments_order_by

urlpatterns = [
    path('', index, name='index'),
    path('posts/post_add/', post_add, name='post_add'),
    path('posts/post_reaction/', post_reaction, name='post_reaction'),
    path('posts/post_edit/<int:post_id>/', post_edit, name='post_edit'),
    path('posts/post_delete/<int:post_id>/', post_delete, name='post_delete'),
    path('posts/<int:post_id>/', single_post, name='single_post'),
    path('posts/<int:post_id>/order_by/',
         comments_order_by, name='comments_order_by'),
]

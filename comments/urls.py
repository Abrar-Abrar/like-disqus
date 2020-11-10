from django.urls import path
from .views import comment_add, comment_edit, comment_delete, comment_reaction

urlpatterns = [
    path('<int:post_id>/comment/', comment_add, name='comment_add'),
    path('comment_edit/<int:comment_id>/',
         comment_edit, name='comment_edit'),
    path('comment_delete/<int:comment_id>/',
         comment_delete, name='comment_delete'),
    path('comment_reaction/', comment_reaction, name='comment_reaction'),
]

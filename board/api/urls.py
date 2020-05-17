from django.urls import path
from . import views

urlpatterns = [
    path("posts/", views.PostListView.as_view()),
    path("posts/<int:pk>/", views.PostDetailView.as_view()),
    path("posts/create/", views.PostCreateView.as_view()),
    path("posts/update/<int:pk>/", views.PostUpdateView.as_view()),
    path("posts/delete/<int:pk>/", views.PostDeleteView.as_view()),
    path("comments/", views.CommentsListView.as_view()),
    path("comments/create", views.CommentsCreateView.as_view()),
    path("comments/update/<int:pk>/", views.CommentsUpdateView.as_view()),
    path("comments/delete/<int:pk>/", views.CommentsDeleteView.as_view()),
    path("upvotes/", views.AddUpvotes.as_view()),
    path("delete_all/", views.DeleteVotes.as_view()),
]
#
#

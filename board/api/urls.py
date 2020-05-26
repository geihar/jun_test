from django.urls import path

from . import views

urlpatterns = [
    path("posts/", views.PostViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "posts/<int:pk>/",
        views.PostViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
    path("comments/", views.CommentsViewSet.as_view({"post": "create"})),
    path(
        "comments/<int:pk>/",
        views.CommentsViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
    path("upvotes/", views.AddUpvote.as_view()),
]
#
#

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions, viewsets
from django.db import models


from .permissions import IsOwnerOrReadOnly
from .services import get_client_ip
from ..models import Post, Comment
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    CommentsCRUDlSerializer,
    PostCRUDlSerializer,
    CreateUpvoteSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().annotate(votes=models.Count(models.F("post_upvote")))
    serializer_class = PostCRUDlSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = Post.objects.all().annotate(
            votes=models.Count(models.F("post_upvote"))
        )
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PostDetailSerializer(instance)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ["create"]:
            self.permission_classes = [
                permissions.IsAuthenticated,
            ]
        elif self.action in [
            "update",
            "partial_update",
        ]:
            self.permission_classes = [
                IsOwnerOrReadOnly,
            ]
        elif self.action in ["destroy"]:
            self.permission_classes = [
                permissions.IsAdminUser,
            ]
        else:
            self.permission_classes = [
                permissions.AllowAny,
            ]
        return super(self.__class__, self).get_permissions()


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsCRUDlSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in ["create"]:
            self.permission_classes = [
                permissions.IsAuthenticated,
            ]
        elif self.action in [
            "update",
            "partial_update",
            "destroy",
        ]:
            self.permission_classes = [
                IsOwnerOrReadOnly,
            ]
        else:
            self.permission_classes = [
                permissions.AllowAny,
            ]
        return super(self.__class__, self).get_permissions()


class AddUpvote(generics.CreateAPIView):
    serializer_class = CreateUpvoteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions

from .permissions import IsOwnerOrReadOnly
from .servises import get_client_ip
from django.db import models

from ..models import Post, Comments, Upvotes
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    CommentsSerializer,
    CommentsCRUDlSerializer,
    PostCRUDlSerializer,
    CommentsListSerializer,
    CreateUpvoteSerializer,
)


class PostListView(generics.ListAPIView):

    serializer_class = PostListSerializer
    comments = CommentsSerializer(many=True)

    def get_queryset(self):
        movies = Post.objects.all().annotate(
            votes=models.Count(models.F("post_upvote"))
        )
        return movies


class PostDetailView(generics.RetrieveAPIView):

    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class PostCreateView(generics.CreateAPIView):

    serializer_class = PostCRUDlSerializer
    permission_classes = (permissions.IsAuthenticated,)


class PostUpdateView(generics.UpdateAPIView):

    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class PostDeleteView(generics.DestroyAPIView):

    serializer_class = PostCRUDlSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        queryset = Post.objects.filter(id=self.kwargs["pk"])
        return queryset


class CommentsCreateView(generics.CreateAPIView):

    serializer_class = CommentsCRUDlSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CommentsUpdateView(generics.UpdateAPIView):

    queryset = Comments.objects.all()
    serializer_class = CommentsCRUDlSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class CommentsDeleteView(generics.DestroyAPIView):

    serializer_class = CommentsCRUDlSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        queryset = Comments.objects.filter(id=self.kwargs["pk"])
        return queryset


class CommentsListView(generics.ListAPIView):
    serializer_class = CommentsListSerializer

    def get_queryset(self):
        comments = Comments.objects.all()
        return comments


class AddUpvotes(generics.CreateAPIView):

    serializer_class = CreateUpvoteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class DeleteVotes(APIView):

    comments = Upvotes.objects.all().delete()

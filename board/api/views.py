from rest_framework import generics
from rest_framework.views import APIView

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


class PostUpdateView(generics.UpdateAPIView):

    queryset = Post.objects.all()
    serializer_class = PostCRUDlSerializer
    permission_classes = [IsOwnerOrReadOnly]


class PostDeleteView(generics.DestroyAPIView):

    serializer_class = PostCRUDlSerializer

    def get_queryset(self):
        queryset = Post.objects.filter(id=self.kwargs["pk"])
        return queryset


class CommentsCreateView(generics.CreateAPIView):

    serializer_class = CommentsCRUDlSerializer


class CommentsUpdateView(generics.UpdateAPIView):

    queryset = Comments.objects.all()
    serializer_class = CommentsCRUDlSerializer


class CommentsDeleteView(generics.DestroyAPIView):

    serializer_class = CommentsCRUDlSerializer

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

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class DeleteVotes(APIView):

    comments = Upvotes.objects.all().delete()

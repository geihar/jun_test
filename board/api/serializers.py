from rest_framework import serializers
from django.contrib.auth.models import User

from ..models import Post, Comment, Upvote


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class FilterCommentsSerializer(serializers.ListSerializer):
    def to_representation(self, instance):
        data = instance.filter(parent=None)
        return super().to_representation(data)


class CommentsSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterCommentsSerializer
        model = Comment
        fields = ("author", "content", "children")


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
        )


class PostListSerializer(serializers.ModelSerializer):

    author = AuthorSerializer(read_only=True)
    votes = serializers.IntegerField()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "slug",
            "author",
            "votes",
        )


class PostDetailSerializer(serializers.ModelSerializer):

    author = AuthorSerializer(read_only=True)
    comment = CommentsSerializer(many=True)
    votes = serializers.IntegerField()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "slug",
            "creation_date",
            "author",
            "comment",
            "votes",
        )


class CommentsCRUDlSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("__all__")
        read_only_fields = ("author",)


class PostCRUDlSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ("__all__")
        read_only_fields = ("slug",)


class CreateUpvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upvote
        fields = ("post",)

    def create(self, validated_data):
        upvotes, _ = Upvote.objects.update_or_create(
            ip=validated_data.get("ip", None), post=validated_data.get("post", None),
        )
        return upvotes

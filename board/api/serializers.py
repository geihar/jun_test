from rest_framework import serializers
from django.contrib.auth.models import User

from ..models import Post, Comments, Upvotes


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
        model = Comments
        fields = ('author', 'content', 'children')


class CommentsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = ('id', 'author', 'content',)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', )


class PostListSerializer(serializers.ModelSerializer):

    author = UserSerializer(read_only=True)
    votes = serializers.IntegerField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'votes' )


class PostDetailSerializer(serializers.ModelSerializer):

    author = UserSerializer(read_only=True)
    comment = CommentsSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'creation_date', 'upvotes', 'author', 'comment')


class CommentsCRUDlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields =('__all__',)


class PostCRUDlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields =('__all__',)

class CreateUpvoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Upvotes
        fields = ('post',)

    def create(self, validated_data):
        upvotes, _ = Upvotes.objects.update_or_create(
            ip=validated_data.get('ip', None),
            post=validated_data.get('post', None),

        )
        return upvotes
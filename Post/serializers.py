from . models import Post
from rest_framework import serializers
from  Comment.serializers import CommentSerializer
class PostSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    comments=CommentSerializer(many=True,read_only=True)
    post_image=serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True,)
    class Meta:
        model = Post
        fields = ['id', 'content','post_image','category','post_date','comments','owner']
from rest_framework import serializers
from . models import Comment
class CommentSerializer(serializers.ModelSerializer):
    commented_by = serializers.ReadOnlyField(source='owner.username')
    comment_image=serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True)
    class Meta:
        model = Comment
        fields = ['id', 'comment','comment_image','comment_date','commented_by']
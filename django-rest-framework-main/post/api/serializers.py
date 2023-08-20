from rest_framework import serializers
from post.models import Post

#Serializer ile

# class PostSerializer (serializers.Serializer):
#     title = serializers.CharField(max_length=200)
#     content = serializers.CharField(max_length=200)

#ModelSerializer ile

class PostSerializer (serializers.ModelSerializer):
    #21 **********
    url = serializers.HyperlinkedIdentityField(view_name='post:detail', lookup_field='slug')
    #****** altta slug'i silip url yaptik
    #22 *********
    username = serializers.SerializerMethodField()
    def get_username(self,obj):
        return str(obj.user.username)
    #********* alttaki user yerine username yazdik
    class Meta:
        model = Post
        fields = [
            'username',
            'title',
            'content',
            'image',
            'url',
            'created',
            'modified_by',
        ]

class PostUpdateCreateSerializer (serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'image',
        ]
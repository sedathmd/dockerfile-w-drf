from django.contrib.auth.models import User
from rest_framework import serializers
from comment.models import Comment
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from post.models import Post


class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        #fields = [] bunun yerine exclude yapip icinde yazan haric hepsini kabul et
        exclude = ['created']

    #validation islemi/ parent yoksa yorum olusturur varsa ve post ile ayniysa da olusturur
    #aksi halde hata verir
    def validate(self, attrs):
        if (attrs["parent"]):
            if attrs["parent"].post != attrs["post"]:
                raise serializers.ValidationError("something went wrong")
        return attrs

###28 ic ice serializer
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'id']

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'id']

#replies altinda cagirilir
#################
class CommentListSerializer(ModelSerializer):
    replies = SerializerMethodField()
    user = UserSerializer()
    post = PostSerializer()
    class Meta:
        model = Comment
        fields = '__all__'

        #bu sekilde de tek satir ile yan tablo cekebiliriz ama safe degil
        #kullanici sifresi gozukuyor. Onun yerine üstteki gibi yapariz
        #depth = 1

    def get_replies(self, obj):
        if obj.any_children:
            return CommentListSerializer(obj.children(), many=True).data


class CommentUpdateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            #sadece content'i degis. Silmede bir seye gerek yok zaten
            'content'
        ]

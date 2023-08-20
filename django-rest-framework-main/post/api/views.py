from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (ListAPIView,
                                     RetrieveAPIView,
                                     RetrieveUpdateAPIView,
                                     CreateAPIView)
from rest_framework.mixins import DestroyModelMixin

from post.api.paginations import PostPagination
from post.api.permissions import IsOwner
from post.api.serializers import PostSerializer, PostUpdateCreateSerializer
from post.models import Post
from rest_framework.permissions import IsAuthenticated

#listemele icin
class PostListAPIView(ListAPIView):
    #queryset = Post.objects.all()
    #postlarin icerisindeki verilerin hepsini getir
    serializer_class = PostSerializer
    pagination_class = PostPagination
    #***********************19
    #draft'ta olmayanlari gosterir
    def get_queryset(self):
        queryset = Post.objects.filter(draft=False)
        return queryset

    #filtreleme ve siralama
    filter_backends = [SearchFilter, OrderingFilter]
    #sadece bunlarda arama yapar
    search_fields = ['title','content']
    # localhost:8000/api/post/list?search=...  (aranacak kelime)
    # localhost:8000/api/post/list?ordering=user  (siralanacak alan)
    # localhost:8000/api/post/list?search=...&ordering=...

    #***********************19son

    #42*****************ScopedRateThrottle
    #throttle_scope = 'sedat'
    #************************************
class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # slug'a gore detail'a git
    lookup_field = 'slug'

# class PostDeleteAPIView(DestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     lookup_field = 'slug'
#     permission_classes = [IsOwner]

#RetrieveUpdateAPIView yaptik cunku degisecek field'ları dolu olarak getirir
class PostUpdateAPIView(RetrieveUpdateAPIView, DestroyModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostUpdateCreateSerializer
    lookup_field = 'slug'

    #guncelleyen son kullaniciyi gosterir
    #baska kullanicinin postunu da günceller safe degil
    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)
    #bu üstekinin cozumu. Sadece postun sahibi ve admin(superuser) degistirebilir
    permission_classes = [IsOwner]

    #30 delete sayfasini update sayfasine entegre etme
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
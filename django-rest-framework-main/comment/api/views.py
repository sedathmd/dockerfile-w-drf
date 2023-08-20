from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.mixins import  DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from comment.api.paginations import CommentPagination
from comment.api.permissions import IsOwner
from comment.models import Comment
from comment.api.serializers import CommentCreateSerializer, CommentListSerializer, CommentUpdateDeleteSerializer


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentListAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    pagination_class = CommentPagination

    #parenti olmayanlari gonderdi
    # def get_queryset(self):
    #     return Comment.objects.filter(parent=None)
    #alttaki ile degistirdik. Aradigimiz postun altindaki yorumlari gormek icin

    #arama yapilan id'ye gore sirala
    #arama yapilmiyorsa hepsini getir (parent olmayan)
    def get_queryset(self):
        queryset = Comment.objects.filter(parent=None)
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(post=query)
        return queryset

# class CommentDeleteAPIView(DestroyAPIView, UpdateModelMixin, RetrieveModelMixin):
#     queryset = Comment.objects.all()
#     serializer_class = CommentUpdateDeleteSerializer
#     lookup_field = 'pk'
#     permission_classes = [IsOwner]
#
#     #29 UpdateModalMixin, RetrieveModalMixin kullanimi
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#     ###########

#retrieveapiview update ederken eski yorumun default olarak gelmesi icin
class CommentUpdateAPIView(UpdateAPIView, RetrieveAPIView, DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentUpdateDeleteSerializer
    lookup_field = 'pk'
    permission_classes = [IsOwner]

    #30 DestroyModalMixin Kullanimi yukaridakinden daha kullanisli
    # ayri ayri delete ve update yapmaya gerek kalmadi. /delete sayfasini kullanimdan kaldirdik
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
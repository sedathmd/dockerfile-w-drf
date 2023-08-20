from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    # bu arasi sonradan eklendi. giris yapmamis kullanicinin bu sayfalara girmemesi icin
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    # ^^^^^^^^^^^^^^^^^^^^^^ has_object_permissiondan farki once calismasi ve her türlü calismasi
    message= 'you must be the owner of this object.'
    def has_object_permission(self, request, view, obj):
        #post sahibi ya da superuser olup olmadigini kontrol eder
        return (obj.user == request.user) or request.user.is_superuser
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    #her bir blog yazisi olusturuldugunda bunun bir useri olacak
    #on_delete durumunda kullaniciyla iliskilendirilen tüm blog yazilari da silinecek
    title = models.CharField(max_length=120)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()
    slug = models.SlugField(unique=True, max_length=150, editable=False)
    image = models.ImageField(upload_to='post', null=True, blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modified_by')
    #id ye gore sirala
    class Meta:
        ordering = ["-id"]
    def get_slug(self):
        slug = slugify(self.title.replace("ı", "i"))
        unique = slug
        number = 1
        while Post.objects.filter(slug=unique).exists():
            unique = '{}-{}'.format(slug, number)
            number += 1
        return unique

    # alt tarafta daha once bir post olusturulmamissa ilk seferde id olusturur
    # daha sonraki duzenlemelerde burasi tetikleneceginden yeni id olusturulmaz
    def save(self, *args, **kvargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        self.slug = self.get_slug()
        return super(Post, self).save(*args, **kvargs)

    def __str__(self):
        return self.title
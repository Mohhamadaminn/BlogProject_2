from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=100)
    slug =  models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


    def __str__(self):
            return self.title
    
    def get_absolute_url(self):
        return reverse("posts_list", kwargs={"pk": self.pk})
    

    def save(self, *args, **kwargs):
         if not self.slug:
              base_slug = slugify(self.title)
              slug = base_slug
              num = 1
              # make sure slug is unique.
              while Post.objects.filter(slug=slug).exists():
                   slug = f"{base_slug} - {num}"
                   num += 1
              self.slug = slug
         super().save(*args, **kwargs)


   
class Profile(models.Model):
     user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
     bio = models.TextField(blank=True)
     avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
     website = models.URLField(blank=True)

     def __str__(self):
          return f"{self.user.username}'s Profile"
     
     def get_absolute_url(self):
          return reverse('user_profile', kwargs={'username': self.user.username})

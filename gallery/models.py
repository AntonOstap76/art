from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Picture(models.Model):
    title = models.CharField(max_length=255, null=False,blank=False)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='arts/', null=False,blank=False )
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    liked = models.ManyToManyField(User, related_name="liked_items", blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    picture=models.ForeignKey(Picture, on_delete=models.CASCADE, related_name='comments')
    content=models.CharField(max_length=255)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('picture', 'user')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='images/profile.svg')
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


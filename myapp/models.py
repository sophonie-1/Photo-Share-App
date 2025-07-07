from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name =models.CharField(max_length=200)

    def __str__(self):
        return self.name

class CommentModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    photo=models.ForeignKey('Photo',on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    likes=models.IntegerField(default=0)
    dislikes=models.IntegerField(default=0)
    comment=models.CharField(max_length=500)
    

    def __str__(self):
        return f"Comment by {self.user.username if self.user else 'Anonymous'} on {self.date.strftime('%Y-%m-%d')}"

    
    
class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    image =models.ImageField()
    description =models.TextField()
    date =models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.description[:50]  # Return first 50 characters of description

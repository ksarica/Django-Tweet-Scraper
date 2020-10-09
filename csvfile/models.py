from django.db import models


# Create your models here.

class Tweet(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=150)
    date = models.CharField(max_length=30)
    text = models.TextField()
    comment = models.CharField(max_length=30)
    retweet = models.CharField(max_length=30)
    like = models.CharField(max_length=30)

    class Meta:
        db_table = 'tweets'

    def __str__(self):
        return '(' + str(self.id) + ')' + self.author

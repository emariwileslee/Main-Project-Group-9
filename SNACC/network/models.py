from django.db import models

class Account(models.Model):
    username = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, blank=True, null = True)
    bio = models.CharField(max_length=300, blank=True, null = True)
    average_likes = models.IntegerField(blank=True, null=True)
    num_followers = models.IntegerField()
    num_following = models.IntegerField()

class Connection(models.Model):
    to = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='to_connections')
    fro = models.ForeignKey(Account, on_delete=models.CASCADE, related_name = 'fro_connections')
    connection_type = models.CharField(max_length=20)
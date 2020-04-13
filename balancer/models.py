from django.db import models

# Create your models here.

class Match(models.Model):
    name = models.CharField(max_length=200)
    match_id = models.IntegerField
    match_date = models.DateTimeField(auto_now_add=True)
    match_played = models.BooleanField(default=False)
    
    objects = models.Manager()

class Player(models.Model):
    match = models.ForeignKey(Match, related_name='players', on_delete=models.CASCADE)

    steam_id = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200)
    rating = models.IntegerField(default=1000)
    color = models.CharField(max_length=200, blank=True, null=True)
    civ = models.CharField(max_length=200, blank=True, null=True)
    
    objects = models.Manager()

    class Meta:
        unique_together = ['match', 'steam_id']
        ordering = ['color']

    def __str__(self):
        return '%s: %s' % (self.rating, self.name)


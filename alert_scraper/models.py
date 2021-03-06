from django.db import models


class ScrapedAlert(models.Model):
    timestamp = models.DateTimeField()
    alert = models.TextField()
    alert_type = models.CharField(max_length=200)
    alert_data = models.FileField(null=True, upload_to='alerts')
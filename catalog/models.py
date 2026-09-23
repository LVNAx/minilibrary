import uuid
from django.db import models

# Create your models here.
class Book(models.Model):
    CATEGORY = [
        ('fiksi', 'Fiksi'),
        ('non-fiksi', 'Non-fiksi'),
        ('komik', 'Komik'),
        ('referensi', 'Referensi')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY, default='fiksi')
    synopsis = models.TextField() # Ini itu by default udah langsung wajib ada isinya
    pages = models.PositiveIntegerField()
    cover_url = models.URLField(blank=True)
    is_available = models.BooleanField(default=True)
    published_at = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title
    
    @property
    def is_thick(self):
        return self.pages > 300
        
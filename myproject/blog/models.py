# Verileri veritabanında saklamak için burayı kullanırız. 

from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200) # Başlık
    content = models.TextField() # İçerik
    created_at = models.DateTimeField(auto_now_add=True) # Oluşturulma tarihi

    def __str__(self):
        return self.title # Admin panelinde başlığı göstermek için
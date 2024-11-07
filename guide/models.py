from django.db import models
from tinymce import models as tinymce_models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
    
class TravelGuide(models.Model):
    CATEGORY_CHOICES = (
        ('Nepal Travel Info','Nepal Travel Info'),
        ('Trekking Info','Trekking Info'),
    )

    name = models.CharField(max_length=200) 
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES,default='Nepal Travel Info')
    slug = models.CharField(max_length=300)
    title = models.CharField(max_length=500)
    guide_duration_to_read = models.CharField(max_length=100,blank=True)
    thumbnail_image = models.FileField()
    thumbnail_image_alt_description = models.CharField(max_length=300)
    guide_content = tinymce_models.HTMLField(blank=True)
    meta_title = models.CharField(max_length=200)
    meta_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title



@receiver(pre_save, sender=TravelGuide)
def update_slug(sender, instance, **kwargs):
    if not instance.pk:  # This is a new instance
        instance.slug = slugify(instance.name)
    elif (
        not instance.slug or instance.name != sender.objects.get(pk=instance.pk).name
    ):
        instance.slug = slugify(instance.name)
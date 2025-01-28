from django.db import models
from django.contrib.auth.models import User



class Hashtag(models.Model):
    name = models.CharField(max_length=100)  
   

    def __str__(self):
        return self.name



class TODOListModel(models.Model):
    status_choices=[('Completed','Completed'),
                    ('In Progress','In Progress')
            
            ]
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    list_name=models.CharField(max_length=50)
    list_description=models.CharField(max_length=50)
    list_status=models.CharField(max_length=20,choices=status_choices,default="In Progress")
    created_at = models.DateTimeField(auto_now_add=True) 
    modified_at = models.DateTimeField(auto_now=True)
    hashtags=models.ManyToManyField(Hashtag, related_name='todos', blank=True)
    


    def __str__(self):
        return f"{self.list_name}"


    class Meta:
        verbose_name='TODO List'
        verbose_name_plural='TODO Lists'

    

    def save(self, *args, **kwargs):
        # Check if the object is being created (pk is None)
        if self.pk is None:
            self.list_status = 'In Progress'

        super().save(*args, **kwargs)



    


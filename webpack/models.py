from django.db import models


# Create your models here.


class Notice(models.Model):
    name = models.CharField(max_length=20)
    context = models.CharField(max_length=180)
    cc_from = models.CharField(max_length=20)
    add_date = models.DateField(auto_now_add=True)
    notice_date = models.DateField()
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE, )

    def __str__(self):
        return self.context


class Contact(models.Model):
    name = models.CharField(max_length=20)
    tel = models.CharField(max_length=20)
    email = models.EmailField()
    depart = models.CharField(max_length=20)
    wxuid = models.CharField(max_length=100,default='uid_')
    wxname = models.CharField(max_length=40,default='')
    #frq_days = models.IntegerField(default=1)
    #bef_days = models.IntegerField(default=3)

    def __str__(self):
        return self.name

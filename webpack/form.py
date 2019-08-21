from django import forms


class AddNotice(forms.Form):
    name = forms.ChoiceField(required=True,choices=[
        ('孙睿谦', '孙睿谦'),
        ('张晗', '张晗')]
    )
    context = forms.CharField(required=True,max_length=180)
    notice_date = forms.DateField()


class AddContact(forms.Form):
    name = forms.CharField(max_length=20)
    tel = forms.CharField(max_length=20)
    email = forms.EmailField()
    depart = forms.CharField(max_length=20)

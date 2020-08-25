from django import forms
from .models import TimeTable, ClassRoom
from django.forms import modelformset_factory

class TableForm(forms.ModelForm):
   subject = forms.CharField(max_length=64, required=False)

   class Meta:
      model = TimeTable
      fields = ['id', 'classRoom', 'subject']

# class ClassRoomChoiceField(forms.ModelChoiceField):
#    def label_from_instance(self, obj):
#       return "{} {}", (obj.classGrade, obj.classNumber)

# class ClassRoomForm(forms.ModelForm):
#    classRoomNumber = ClassRoomChoiceField(queryset=ClassRoom.objects.all())
#    class Meta:
#       model = ClassRoom
#       fields=['classGrade', 'classNumber']
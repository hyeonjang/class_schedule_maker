from django.forms import modelformset_factory
from django import forms

from .models import TimeTable, ClassRoom

class TableForm(forms.ModelForm):
   subject = forms.CharField(max_length=64, required=False)

   class Meta:
      model = TimeTable
      fields = ['id', 'classRoom', 'subject', 'weekday']
      widgets = {
        'weekday': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'week'}),
      }

# class ClassRoomChoiceField(forms.ModelChoiceField):
#    def label_from_instance(self, obj):
#       return "{} {}", (obj.classGrade, obj.classNumber)

# class ClassRoomForm(forms.ModelForm):
#    classRoomNumber = ClassRoomChoiceField(queryset=ClassRoom.objects.all())
#    class Meta:
#       model = ClassRoom
#       fields=['classGrade', 'classNumber']
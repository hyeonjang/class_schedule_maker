from django.shortcuts import render, redirect
from .forms import TableForm
from .models import TimeTable

def classroom(request):
    if request.POST:
        form = TableForm(request.POST)
        return redirect('accounts/login.html')
    else:
        form = TableForm()
    return render(request, 'timetable/classroom.html', {'form': form} )

# @@todo 2-array;
def subject(request):
    if request.POST:
        list_form = [[0]*5]*8
        for row in range(8):
            for col in range(5):
                form = TableForm(request.POST)
                if form.is_valid():
                    print("done")
                    form.save()
                else:
                    print(form.errors)
                    print("yet")
                list_form[row][col] = form
        return render(request, 'timetable/subject.html', {'list_form': list_form } )
    else: 
        form = TableForm()
        return render(request, 'timetable/subject.html', {'list_form': form } )

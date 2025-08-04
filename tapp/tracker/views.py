from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Project, TimeEntry

from .forms import TimeEntryForm
from django.shortcuts import redirect

from django.db.models import Sum





# Create your views here.



@login_required
def dashboard(request):
    projects = Project.objects.all()
    entries = TimeEntry.objects.filter(user=request.user)
    
    project_hours = {}
    for project in projects:
        total_duration = entries.filter(project=project).aggregate(Sum('duration'))['duration__sum']
        if total_duration:
            hours = round(total_duration,2)
        else:
            hours=0
        project_hours[project] = hours



    
    time_entries = TimeEntry.objects.filter(user=request.user)

   
    return render(request, 'tracker/dashboard.html', {
        'projects': projects,
        'time_entries': time_entries
    })


from .forms import TimeEntryForm
from django.shortcuts import redirect
from datetime import datetime, timedelta


@login_required
def add_time_entry(request):
    if request.method == 'POST':
        form = TimeEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.date = form.cleaned_data['date']

            start = datetime.combine(entry.date, entry.start_time)
            end = datetime.combine(entry.date, entry.end_time)

            if end < start:
                end += timedelta(days=1)

            duration = (end - start).total_seconds() / 3600 
            entry.duration = round(duration, 2)


            entry.save()
            return redirect('dashboard')
    else:
        form = TimeEntryForm()

    
    return render(request, 'tracker/add_time_entry.html', {'form': form})

from datetime import timedelta
from django.shortcuts import get_object_or_404, redirect, render
from .models import TimeEntry
from .forms import TimeEntryForm  


def edit_time_entry(request, entry_id):
    entry = get_object_or_404(TimeEntry, id=entry_id, user=request.user)
    if request.method == 'POST':
        form = TimeEntryForm(request.POST, instance=entry)
        if form.is_valid():
            entry = form.save(commit=False)

            if entry.start_time and entry.end_time:
                start = datetime.combine(datetime.today(), entry.start_time)
                end = datetime.combine(datetime.today(), entry.end_time)

                if end < start:
                    end += timedelta(days=1)  

                duration = end - start
                entry.duration = round(duration.total_seconds() / 3600, 2)  
                
            entry.save()
            entry.save()
            return redirect('dashboard')
    else:
        form = TimeEntryForm(instance=entry)
    return render(request, 'edit_time_entry.html', {'form': form})


from django.shortcuts import get_object_or_404, redirect

@login_required
def delete_time_entry(request, entry_id):
    entry = get_object_or_404(TimeEntry, id=entry_id, user=request.user)
    entry.delete()
    return redirect('dashboard')

from .forms import ProjectForm


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            form.save()
            return redirect('dashboard')
    else:
        form = ProjectForm()
    return render(request, 'tracker/create_project.html', {'form': form})



from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Project

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, created_by=request.user)
    project.delete()
    return redirect('dashboard')

from .models import TimeEntry, Project
from .forms import TimeEntryForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def employee_entry(request):
    if request.user.userprofile.is_employee:
        if request.method == 'POST':
            form = TimeEntryForm(request.POST)
            if form.is_valid():
                entry = form.save(commit=False)
                entry.user = request.user
                entry.save()
                return redirect('employee_success')
        else:
            form = TimeEntryForm()
        return render(request, 'tracker/employee_entry.html', {'form': form})
    else:
        return redirect('dashboard')  # send admins to admin dashboard
    

from django.contrib.auth.decorators import login_required

@login_required
def employee_entry(request):
    ...


from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect

from django.contrib.auth.decorators import user_passes_test

def is_employee(user):
    return user.groups.filter(name='Employees').exists()

@login_required
@user_passes_test(is_employee)
def employee_entry(request):
    if request.method == 'POST':
        form = TimeEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.date = form.cleaned_data['date']

            start = datetime.combine(entry.date, entry.start_time)
            end = datetime.combine(entry.date, entry.end_time)
            if end < start:
                end += timedelta(days=1)

            duration = end - start
            entry.duration = duration
            entry.save()
            return redirect('employee_success')  # show a simple success page
    else:
        form = TimeEntryForm()

    return render(request, 'tracker/employee_entry.html', {'form': form})

@login_required
def dashboard(request):
    if is_employee(request.user):
        return redirect('employee_entry')
    projects = Project.objects.all()
    entries = TimeEntry.objects.filter(user=request.user)
    
    project_hours = {}
    for project in projects:
        total_duration = entries.filter(project=project).aggregate(Sum('duration'))['duration__sum']
        if total_duration:
            hours = round(total_duration,2)
        else:
            hours=0
        project_hours[project] = hours



    
    time_entries = TimeEntry.objects.filter(user=request.user)

   
    return render(request, 'tracker/dashboard.html', {
        'projects': projects,
        'time_entries': time_entries
    })




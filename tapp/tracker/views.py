from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Project, TimeEntry

from .forms import TimeEntryForm
from django.shortcuts import redirect



# Create your views here.



@login_required
def dashboard(request):
    projects = Project.objects.all()
    time_entries = TimeEntry.objects.filter(user=request.user)
    return render(request, 'tracker/dashboard.html', {
        'projects': projects,
        'time_entries': time_entries
    })


from .forms import TimeEntryForm
from django.shortcuts import redirect

@login_required
def add_time_entry(request):
    if request.method == 'POST':
        form = TimeEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('dashboard')  # make sure this matches your dashboard URL name
    else:
        form = TimeEntryForm()
    return render(request, 'tracker/add_time_entry.html', {'form': form})

from datetime import timedelta
from django.shortcuts import get_object_or_404, redirect, render
from .models import TimeEntry
from .forms import TimeEntryForm  # make sure this import exists

def edit_time_entry(request, entry_id):
    entry = get_object_or_404(TimeEntry, id=entry_id, user=request.user)
    if request.method == 'POST':
        form = TimeEntryForm(request.POST, instance=entry)
        if form.is_valid():
            entry = form.save(commit=False)
            if entry.start_time and entry.end_time:
                entry.duration = entry.end_time - entry.start_time
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

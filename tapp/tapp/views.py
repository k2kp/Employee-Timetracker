from django.shortcuts import render, redirect
from tracker.forms import TimeEntryForm

def time_entry_view(request):
    if request.method == 'POST':
        form = TimeEntryForm(request.POST)
        if form.is_valid():
            time_entry = form.save(commit=False)
            time_entry.user = request.user  # assumes user is logged in
            time_entry.save()
            return redirect('success')  # placeholder, we’ll define this
    else:
        form = TimeEntryForm()
    
    return render(request, 'time_entry.html', {'form': form})

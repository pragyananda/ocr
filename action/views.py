from django.shortcuts import render,redirect
from .models import UploadedFile
import traceback
from django.http import JsonResponse
from django.http import Http404
from django.contrib import messages
# Create your views here.
from django.core import serializers
from django.views.decorators.http import require_POST
import json


@require_POST
def update_cell(request):
    cell_id = request.POST.get('cell_id')
    data_to_update = json.loads(request.POST.get('data_to_update'))

    try:
        uploaded_file = UploadedFile.objects.get(id=cell_id)
        for field, value in data_to_update.items():
            setattr(uploaded_file, field, value)  # Update the fields based on the data
        uploaded_file.save()

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error_message': str(e)})


def index(request):
    uploaded_rows = UploadedFile.objects.filter(finalized=False).order_by('-uploaded_at')
    
    # Modify the image filenames
    for row in uploaded_rows:
        row.file.name = row.file.name.split('/')[-1]  # Get only the filename


    return render(request, 'index.html', {'uploaded_rows': uploaded_rows})


def archive(request):
    archived_images = UploadedFile.objects.filter(finalized=True)
    for row in archived_images:
        row.file.name = row.file.name.split('/')[-1]
    return render(request, 'archive.html', {'archived_images':archived_images})


def uploadfile(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('file')
        uploaded_count = 0
        
        for uploaded_file in uploaded_files:
            try:
                new_uploaded_file = UploadedFile(file=uploaded_file)
                new_uploaded_file.save()
                uploaded_count += 1
            except Exception as e:
                traceback.print_exc()
        
        if uploaded_count > 0:
            messages.success(request, f'{uploaded_count} files uploaded successfully.')
        else:
            messages.error(request, 'No files were uploaded.')

    rows = UploadedFile.objects.all()
    return redirect('home')


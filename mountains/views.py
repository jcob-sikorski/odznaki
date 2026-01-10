# mountains/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PhotoUploadForm
from .models import Photo, Mountain

@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect('profile')
    else:
        form = PhotoUploadForm()
    return render(request, 'upload.html', {'form': form})

@login_required
def profile(request):
    user_photos = Photo.objects.filter(user=request.user).order_by('-uploaded_at')
    
    # Obliczanie postępu (unikalne zdobyte szczyty)
    visited_ids = user_photos.filter(matched_mountain__isnull=False).values_list('matched_mountain', flat=True)
    visited_mountains = Mountain.objects.filter(id__in=visited_ids).distinct()
    all_mountains_count = Mountain.objects.count()
    
    context = {
        'photos': user_photos,
        'visited_mountains': visited_mountains,
        'progress': f"{visited_mountains.count()} / {all_mountains_count}"
    }
    return render(request, 'profile.html', context)
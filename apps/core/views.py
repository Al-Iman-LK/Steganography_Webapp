import logging
import time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib import messages
from .models import SteganoFile
from .services.steganography.processor import SteganographyProcessor
from .services.steganography.extractor import SteganographyExtractor
from django.utils import timezone
from .forms import SteganoFileForm

logger = logging.getLogger(__name__)

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = SteganoFileForm(request.POST, request.FILES)
        if form.is_valid():
            stegano_file = form.save(commit=False)
            stegano_file.user = request.user
            stegano_file.save()
            return redirect('core:process_file', pk=stegano_file.pk)
    else:
        form = SteganoFileForm()
    return render(request, 'core/upload.html', {'form': form})

@login_required
def upload_for_extraction(request):
    if request.method == 'POST':
        form = SteganoFileForm(request.POST, request.FILES)
        if form.is_valid():
            stegano_file = form.save(commit=False)
            stegano_file.user = request.user
            stegano_file.status = 'completed'
            stegano_file.processed_file = stegano_file.original_file
            stegano_file.save()

            # Immediately extract the message
            try:
                extractor = SteganographyExtractor(stegano_file)
                extracted_message = extractor.extract_message()
                stegano_file.extracted_message = extracted_message
                stegano_file.extraction_date = timezone.now()
                stegano_file.extraction_status = 'completed'
                stegano_file.save()
                
                messages.success(request, 'Message extracted successfully!')
                return render(request, 'core/extraction_result.html', {
                    'file': stegano_file,
                    'extracted_message': extracted_message
                })
            except Exception as e:
                messages.error(request, f'Extraction failed: {str(e)}')
                return redirect('core:upload_for_extraction')
    else:
        form = SteganoFileForm()
    return render(request, 'core/upload_extract.html', {'form': form})

class FileListView(ListView):
    model = SteganoFile
    template_name = 'core/file_list.html'
    context_object_name = 'files'

    def get_queryset(self):
        return SteganoFile.objects.filter(user=self.request.user)

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['recent_files'] = SteganoFile.objects.filter(
                user=self.request.user
            ).order_by('-created_at')[:5]
        return context

@login_required
def process_file(request, pk):
    stegano_file = get_object_or_404(SteganoFile, pk=pk, user=request.user)
    processor = SteganographyProcessor(stegano_file)
    
    if request.method == 'POST':
        message = request.POST.get('message', '')
        try:
            processor.embed_message(message)
            messages.success(request, 'File processed successfully!')
            return redirect('core:file_list')
        except Exception as e:
            messages.error(request, f'Processing failed: {str(e)}')
    
    return render(request, 'core/process.html', {'file': stegano_file})

@login_required
def extract_message(request, pk):
    stegano_file = get_object_or_404(SteganoFile, pk=pk, user=request.user)
    
    if request.method == 'POST':
        try:
            extractor = SteganographyExtractor(stegano_file)
            extracted_message = extractor.extract_message()
            
            stegano_file.extracted_message = extracted_message
            stegano_file.extraction_date = timezone.now()
            stegano_file.extraction_status = 'completed'
            stegano_file.save()
            
            messages.success(request, 'Message extracted successfully!')
            return render(request, 'core/extract.html', {
                'file': stegano_file,
                'extracted_message': extracted_message
            })
        except Exception as e:
            messages.error(request, f'Extraction failed: {str(e)}')
    
    return render(request, 'core/extract.html', {'file': stegano_file})

@login_required
def extract_uploaded_file(request, pk):
    stegano_file = get_object_or_404(SteganoFile, pk=pk, user=request.user)
    
    if request.method == 'POST':
        try:
            extractor = SteganographyExtractor(stegano_file)
            extracted_message = extractor.extract_message()
            
            stegano_file.extracted_message = extracted_message
            stegano_file.extraction_date = timezone.now()
            stegano_file.extraction_status = 'completed'
            stegano_file.save()
            
            messages.success(request, 'Message extracted successfully!')
            return render(request, 'core/extract.html', {
                'file': stegano_file,
                'extracted_message': extracted_message
            })
        except Exception as e:
            messages.error(request, f'Extraction failed: {str(e)}')
    
    return render(request, 'core/extract.html', {'file': stegano_file})

@login_required
def clear_file_history(request):
    if request.method == 'POST':
        user_files = SteganoFile.objects.filter(user=request.user)
        
        for file in user_files:
            try:
                # Close any open file handles
                if hasattr(file.original_file, 'file'):
                    try:
                        file.original_file.file.close()
                    except:
                        pass
                if hasattr(file.processed_file, 'file'):
                    try:
                        file.processed_file.file.close()
                    except:
                        pass

                # Add a small delay to ensure files are released
                time.sleep(0.1)
                
                # Delete files with retries
                for _ in range(3):  # Try up to 3 times
                    try:
                        if file.original_file:
                            file.original_file.delete(save=False)
                        if file.processed_file:
                            file.processed_file.delete(save=False)
                        break
                    except Exception as e:
                        logger.warning(f"Retry deleting file: {str(e)}")
                        time.sleep(0.2)  # Wait before retry
                
            except Exception as e:
                logger.error(f"Error during file cleanup: {str(e)}")
                continue
        
        try:
            # Delete database records
            user_files.delete()
            messages.success(request, 'All file history has been cleared successfully.')
        except Exception as e:
            logger.error(f"Error deleting database records: {str(e)}")
            messages.error(request, 'Some files could not be deleted. Please try again.')
        
        return redirect('core:file_list')
    
    return render(request, 'core/clear_history_confirm.html')

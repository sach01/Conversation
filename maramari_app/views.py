from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def test_page(request):
    return Response({"message": "Welcome to Maramari App API!"})

import csv
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .models import SentencePair
from django.http import JsonResponse

from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import csv
from .models import SentencePair

from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import csv
from .models import SentencePair
import logging

logger = logging.getLogger(__name__)

def import_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        fs = FileSystemStorage(location='media/ensw')
        filename = fs.save(csv_file.name, csv_file)
        file_path = fs.path(filename)

        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                if 'English_sentence' not in reader.fieldnames or 'Kiswahili_sentence' not in reader.fieldnames:
                    return JsonResponse({"error": "CSV file format incorrect. Must contain 'English_sentence' and 'Kiswahili_sentence' headers."}, status=400)

                for row in reader:
                    SentencePair.objects.create(
                        english_sentence=row['English_sentence'],
                        kiswahili_sentence=row['Kiswahili_sentence']
                    )
            return JsonResponse({"message": "CSV data imported successfully!"})
        except Exception as e:
            logger.error(f"Error processing CSV: {str(e)}")
            return JsonResponse({"error": f"Error processing CSV: {str(e)}"}, status=500)

    return render(request, 'import_csv.html')

def list_data(request):
    sentence_pairs = SentencePair.objects.all()
    return render(request, 'list_data.html', {'sentence_pairs': sentence_pairs})


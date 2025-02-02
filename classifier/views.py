from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from inference_sdk import InferenceHTTPClient
from .models import ClassificationResult
import tempfile
import os
from datetime import datetime

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="5GVDg6S1EmX7ka0TYgZy"
)

@csrf_exempt
def classify_waste(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            for chunk in image_file.chunks():
                temp_file.write(chunk)
            temp_path = temp_file.name

        try:
            result = CLIENT.infer(temp_path, model_id="garbage-classification-3/2")
            
            # Save to database
            classification = ClassificationResult(
                image=image_file,
                predictions=result
            )
            classification.save()
            
            os.unlink(temp_path)
            return JsonResponse(result)
        except Exception as e:
            os.unlink(temp_path)
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_history(request):
    results = ClassificationResult.objects.all().order_by('-created_at')
    history = [{
        'id': result.id,
        'image_url': result.image.url,
        'predictions': result.predictions,
        'date': result.created_at.strftime("%Y-%m-%d"),
        'time': result.created_at.strftime("%H:%M:%S")
    } for result in results]
    return JsonResponse(history, safe=False)

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import ClassificationResult

@csrf_exempt
def delete_history_item(request, item_id):
    try:
        item = ClassificationResult.objects.get(id=item_id)
        item.delete()
        return JsonResponse({'status': 'success'})
    except ClassificationResult.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)
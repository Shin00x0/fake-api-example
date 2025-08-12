from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services_upload import generate_url_uploadfiles
from django.core.files.storage import default_storage
# Create your views here.


@api_view(["GET"])
def request_upload(request):
    file_name = request.query_params.get("name")
    file_type = request.query_params.get("type")
    file_size = int(request.query_params.get("size", 0))

    if not file_name or not file_type:
        return Response({"error": "name and type required"}, status=400)

    # Definir límites: si es grande o video → presigned URL
    if file_type in ["video/mp4", "video/mov"] or file_size > 10_000_000:
        presigned_data = generate_url_uploadfiles(file_name, file_type)
        return Response({"mode": "direct", "data": presigned_data})

    # Si es pequeño → subida normal al backend
    return Response({"mode": "backend", "upload_url": "/api/files/upload"})


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        file_obj = request.data.get("file")
        if not file_obj:
            return Response({"error": "No file uploaded"}, status=400)

        file_path = default_storage.save(file_obj.name, file_obj)
        file_url = default_storage.url(file_path)

        return Response({"url": file_url})

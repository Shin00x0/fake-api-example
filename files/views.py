from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services_upload import generate_url_uploadfiles
from django.core.files.storage import default_storage

from rest_framework.viewsets import ModelViewSet

from .models import Document
from .serializers import DocumentSerializer


'''
Par la implementacion de subida de archivos primero:

primero definir que tipo de subida es para eso 
- analizar el tamanio del archivo'
- si el archivo es de < 50 mb lo subiremos por multiparser binario
- si el archivo es de > 50 mb subiremos la carga desde el cliente  y guardaremos la url


'''

from rest_framework.parsers import JSONParser, MultiPartParser,FormParser
from rest_framework import status
from .models import Document


import uuid



ALLOWED_EXTENSIONS = ['pdf', 'jpg', 'png', 'docx']
MAX_FILE_SIZE_MB = 50
MAX_FILES = 5

class DocumentApiView(APIView):
    # minimo autenticacion parser
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        files = request.FILES.get('file')

        if not files:
            return Response({'error': 'no se subieron archivos',},
            status=status.HTTP_400_BAD_REQUEST)
        
        for file in files:

            ext = file.name.split('.')[-1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                return Response({"error": f"Archivo {file.name} no permitido"}, status=status.HTTP_400_BAD_REQUEST)
            if file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
                return Response({"error": f"Archivo {file.name} excede {MAX_FILE_SIZE_MB} MB"}, status=status.HTTP_400_BAD_REQUEST)

            name = f"{uuid.uuid4()}.{ext}" # idenditicicaod rde archivo
            # implementacion de validaciones
            document = Document.objects.create(
                name=name,
                file=file,
                type='local',
            )
        return Response({"message": "archivos subidos correctamente"}, status=status.HTTP_201_CREATED)




class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


'''

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
'''


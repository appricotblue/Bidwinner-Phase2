from django.shortcuts import render
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pdf2image import convert_from_bytes
from datetime import datetime
from django.core.files.base import ContentFile
from io import BytesIO
import pytesseract
from PIL import Image
import string
import secrets

def generate_random_string(length=20):
    characters      = string.ascii_letters + string.digits
    random_string   = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string

@api_view(['POST'])
def appAuthToken(request):
    ## delete all records and insert new one 
    app_auth_token_tb.objects.all().delete()

    random_password = generate_random_string()
    now             = datetime.now()

    insert_data     = app_auth_token_tb(token=random_password,created_at=now,updated_at=now)
    insert_data.save()

    response        =   {
                            "success"   : True,
                            "message"   : "",
                            "random_password":random_password
                        }

    return Response(response)
from PyPDF2 import PdfReader
from pdf2image import convert_from_bytes
from PIL import Image
from django.core.files.base import ContentFile
from wand.image import Image as WandImage
@api_view(['POST'])
def addPdfToImage(request):
    data = request.data
    app_token = data.get('app_token')
    get_token = app_auth_token_tb.objects.first()

    if app_token != get_token.token:
        return Response({"success": False, "message": "Invalid Token or User"})

    pdf_file = request.FILES.get('pdf_file')
    if not pdf_file or not pdf_file.content_type.startswith('application/pdf'):
        return Response({"success": False, "message": "Invalid PDF file provided"})

    now = datetime.now()

    try:
        # Create pdf_data_tb entry
        pdf_data = pdf_data_tb.objects.create(created_at=now, updated_at=now)

        # Process each page of the PDF file
        with WandImage(file=pdf_file, resolution=300) as pdf:
            for i, page in enumerate(pdf.sequence, 1):
                with WandImage(page) as img:
                    # Convert the page to PNG
                    img.format = 'png'
                    png_image_bytes = img.make_blob()

                # Save the image data to the database
                pdf_images_data = pdf_to_image_data_tb.objects.create(
                    pdf_id=pdf_data,
                    title=f'Page {i}',
                    created_at=now,
                    updated_at=now
                )
                # Save the PNG image file
                image_file = ContentFile(png_image_bytes, name=f'page_{i}.png')
                pdf_images_data.image.save(f'page_{i}.png', image_file, save=True)

        response = {
            "success": True,
            "message": "Successfully created",
        }

    except Exception as e:
        return Response({"success": False, "message": f"Error processing PDF: {str(e)}"})

    return Response(response)


@api_view(['POST'])
def listPdfToImage(request):
    data        = request.data
    app_token   = data.get('app_token')
    get_token   = app_auth_token_tb.objects.first()
    
     
    if app_token == get_token.token:

        get_all_pdf_images   = pdf_to_image_data_tb.objects.all()
 
        pdf_images_details    = []
        for details in get_all_pdf_images:  
            pdf_images_details.append({
                             "success"          : True,
                             "pdf_id"           : details.pdf_id.id,
                             "pdf_image_id"     : details.id,
                             "title"            : details.title,
                             "pdf_image"        : details.image.url if details.image else '',
                             "created_at"       : details.created_at,
                             "updated_at"       : details.updated_at
            })
        
        response        =   {
                                "pdf_images_details" : pdf_images_details
                            }
    else:
        response        =   {
                                "success"   : False,
                                "message"   : "Invalid Token",
                            }

    return Response(response)

def extract_text_from_coords(image_path, coords):
    image = Image.open(image_path)

    x1, y1, x2, y2 = coords
    cropped_image = image.crop((x1, y1, x2, y2))

    text = pytesseract.image_to_string(cropped_image)

    return text.strip() or 'N/a'



@api_view(['POST'])
def addAutoRenameImage(request):
    data       = request.data
    app_token  = data.get('app_token')
    get_token  = app_auth_token_tb.objects.first()

    if app_token == get_token.token:

        pdf_id  = request.data.get('pdf_id')
        coords  = request.data.get('coords')
        
        coords_list = coords.split(',')
        
        x1, y1, x2, y2 = map(int, coords_list)

        images = pdf_to_image_data_tb.objects.filter(pdf_id=pdf_id)
        
        for image in images:
            extracted_text  = extract_text_from_coords(image.image.path, (x1, y1, x2, y2))
            image.title     = extracted_text
            image.save()
        
        response =          { 
                                "success"   : True,
                                "message": "Titles updated successfully"
                            }
    else:
        response        =   {
                                "success"   : False,
                                "message"   : "Invalid Token",
                            }
    
    return Response(response)

@api_view(["POST"])
def deletePdf(request):
    data        = request.data 
    app_token   = data.get("app_token")
    get_token   = app_auth_token_tb.objects.first()
    

    if app_token == get_token.token:


        pdf_data      = pdf_data_tb.objects.all()
        pdf_data.delete()
     

       
        response    =   {
                                "success"   : True,
                                "message"   : "Successfully Deleted",
                            }
     

    else: 
        response = {

                       "success"  : False,
                       "message"  : "Invalid Token"
                   }
    
    return Response(response)


@api_view(["POST"])
def deletePdfImage(request):
    data        = request.data 
    app_token   = data.get("app_token")
    get_token   = app_auth_token_tb.objects.first()
    

    if app_token == get_token.token:


        pdf_data      = pdf_to_image_data_tb.objects.all()
        pdf_data.delete()
     

       
        response    =   {
                                "success"   : True,
                                "message"   : "Successfully Deleted",
                            }
     

    else: 
        response = {

                       "success"  : False,
                       "message"  : "Invalid Token"
                   }
    
    return Response(response)
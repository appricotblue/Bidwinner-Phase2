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


@api_view(['POST'])
def addPdfToImage(request):
    data            = request.data
    app_token       = data.get('app_token')
    get_token       = app_auth_token_tb.objects.first()

    if app_token == get_token.token:
        pdf_file    = request.FILES.get('pdf_file')
        now         = datetime.now()

        if pdf_file and pdf_file.content_type == 'application/pdf':
            try:
                images          = convert_from_bytes(pdf_file.read(), dpi=300, size=(800, None), thread_count=4)

                pdf_data        = pdf_data_tb(
                    pdf_file    = pdf_file,
                    created_at  = now,
                    updated_at  = now
                )
                pdf_data.save()

                for i, image in enumerate(images):
                    image_filename  = f'page_{i + 1}.png'
                    page_title      = f'Page {i + 1}'
                    
                    pdf_images_data = pdf_to_image_data_tb(
                        pdf_id      = pdf_data,
                        title       = page_title,
                        created_at  = now,
                        updated_at  = now
                    )
                    pdf_images_data.save()

                    # Save the image file
                    image_io    = BytesIO()
                    image.save(image_io, format='PNG')
                    image_file  = ContentFile(image_io.getvalue(), name=image_filename)
                    pdf_images_data.image.save(image_filename, image_file, save=True)

                response    =   {
                                    "success": True,
                                    "message": "Successfully created",
                                }
            except Exception as e:
                response    =   {
                                    "success": False,
                                    "message": f"Error converting PDF to image: {str(e)}",
                                }
        else:
            response        =   {
                                    "success": False,
                                    "message": "Invalid PDF file provided",
                                }
    else:
        response            =   {
                                    "success": False,
                                    "message": "Invalid Token or User",
                                }

    return Response(response)



@api_view(['POST'])
def listPdfToImage(request):
    data = request.data
    app_token = data.get('app_token')
    get_token = app_auth_token_tb.objects.first()
    
    if app_token == get_token.token:
        get_all_pdf_images = pdf_to_image_data_tb.objects.all()
 
        pdf_images_details = []
        for details in get_all_pdf_images:  
            pdf_images_details.append({
                "success": True,
                "pdf_id": details.pdf_id.id,
                "pdf_image_id": details.id,
                "title": details.title,
                "pdf_image": details.image.url if details.image else '',
                "created_at": details.created_at,
                "updated_at": details.updated_at
            })
        
        # Grouping the images by their PDF IDs
        pdf_images_by_pdf_id = {}
        for pdf_image_detail in pdf_images_details:
            pdf_id = pdf_image_detail['pdf_id']
            if pdf_id not in pdf_images_by_pdf_id:
                pdf_images_by_pdf_id[pdf_id] = []
            pdf_images_by_pdf_id[pdf_id].append(pdf_image_detail)

        response = {
            "pdf_images_by_pdf_id": pdf_images_by_pdf_id
        }
    else:
        response = {
            "success": False,
            "message": "Invalid Token",
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






import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import pdf_to_image_data_tb

@api_view(['POST'])
def find_similar_image(request):
    try:
        data = request.data
        coords = data.get('coords')
        pdf_id = data.get('pdf_id')
        pdf_image_id = data.get('pdf_image_id')
        
        coords_list = coords.split(',')
        x1, y1, x2, y2 = map(int, coords_list)

        # Extract the smaller image from the PNG image based on the provided coordinates
        extracted_image = extract_image_from_coords(pdf_image_id, (x1, y1, x2, y2))

        # Load the images from the PDF image ID
        similar_images = pdf_to_image_data_tb.objects.filter(pdf_id=pdf_id).exclude(id=pdf_image_id)
        similarity_scores = []

        for image_data in similar_images:
            image_array = np.array(Image.open(image_data.image.path))

            # Calculate the structural similarity index
            similarity = ssim(np.array(extracted_image), image_array, multichannel=True)
            similarity_scores.append((image_data.id, similarity))

        # Sort the images by similarity score
        similarity_scores.sort(key=lambda x: x[1], reverse=True)

        # Get the most similar image IDs
        most_similar_image_ids = [image_id for image_id, _ in similarity_scores]

        response = {
            "success": True,
            "most_similar_image_ids": most_similar_image_ids,
            "similar_images_coords": coords_list  # Add coordinates of the extracted image for consistency
        }
    except Exception as e:
        response = {
            "success": False,
            "message": f"Error finding similar images: {str(e)}"
        }

    return Response(response)

def extract_image_from_coords(pdf_image_id, coords):
    pdf_image = pdf_to_image_data_tb.objects.get(id=pdf_image_id)
    image = Image.open(pdf_image.image.path)
    x1, y1, x2, y2 = coords
    cropped_image = image.crop((x1, y1, x2, y2))
    return cropped_image

# Django imports
from django.shortcuts import render, redirect

# Django REST Framework imports
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.parsers import JSONParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Chromadb imports
from vectorDB.chroma_db import ChromaDB

# instantiating ChromaDB
chromadb = ChromaDB()

# CONSTANTS
CHROMA_CLIENT= chromadb.get_client()
COLLECTION = chromadb.get_collection()

@api_view(['GET'])
def heartbeat(request):
    return Response({
        "result": CHROMA_CLIENT.heartbeat(),
    })

@swagger_auto_schema(
    method='get',  # Ensure this matches the HTTP method in @api_view
    manual_parameters=[
        openapi.Parameter(
            name='limit',
            in_=openapi.IN_QUERY,
            description="""Insert the limit for how many records to peek on. (Default is 10)
                            It's recommended not to go over 20""",
            type=openapi.TYPE_INTEGER,
            required=False,
        ),
    ]
)
@api_view(['GET'])
def peek(request):
    try:
        limit = int(request.query_params.get('limit', 10))  # Get the limit query parameter
        return Response({
            "result": COLLECTION.peek(limit= limit),
        })
    except:
        return Response({
            "message": "limit is not a number",
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def list_collections(request):
    return Response({
        "result": CHROMA_CLIENT.list_collections(),
    })

@swagger_auto_schema(
    method='get',  # Ensure this matches the HTTP method in @api_view
    manual_parameters=[
        openapi.Parameter(
            name='query',
            in_=openapi.IN_QUERY,
            description='Insert the text to search the similarity with.',
            type=openapi.TYPE_STRING,
            required=True,
        ),
        openapi.Parameter(
            name='n',
            in_=openapi.IN_QUERY,
            description='Insert the number of similar items. (default is 2)',
            type=openapi.TYPE_INTEGER,
            required=False,
        ),
    ]
)
@api_view(["GET"])
def similar_by_text(request):
    try:
        query = request.query_params.get('query', '')  # Get the "query" query parameter
        n = int(request.query_params.get('n', 2))  # Get the n query parameter
        if query:
            result= get_similar(text=query, n=n)
            return Response({
                "result": result,
            })
            
        else:
            return Response({"result": "There is no text"}, status= status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"result": str(e)}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_similar(text="", n=2):
    if text:
        result= COLLECTION.query(
            query_texts= text,
            n_results= n,
            
        )
        # ids = [int(i) for i in result["ids"][0]]
        # result = get_docs(ids) # Getting the items

    else:
        result= Response({
            "message": "Enter a prompt"
        }, status= status.HTTP_400_BAD_REQUEST)
    
    return result

# def get_docs(ids):
#     try:
#         # Query the COLLECTION to get documents with the given IDs
#         documents = COLLECTION.query(
#             where={"id": {"$in": ids}},
#             include=["documents"]
#         )
        
#         return documents["documents"]
#     except Exception as e:
#         return {
#             "message": str(e)
#         }
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from langchain.tools import tool

import os
import requests
import random

from .agent import Agent

base_url = "http://localhost:8000" if os.environ.get('DEBUG') == "1" else os.environ.get('DEPLOY_URL')
global shopping_cart
shopping_cart = []

@tool
def test_connection() -> str:
    """Use this tool to test the connectivity. Mention the status code"""
    res = requests.get("https://google.com/")
    print("DEBUGGING IS:" + str(os.environ.get('DEBUG')))
    return f"Status code: {res.status_code}, the base url is: {base_url}"

# Removing search items from LLM tools because the model doesn't know how to use it.
@tool
def search_items(search_query: str, n_items=random.randint(3, 7)) -> list:
    """
    This Tool searches for items given a search query which is anything that may lead to an item, \
        whether it is description, relevant items, or a name. Then, returns the top n_items matches.
    This should be your most used tool as it serves most cases.
    """
    res = requests.get(f"{base_url}/api/vector/similar_by_text/?query={search_query}&n={n_items}")
    return res.json()['result']

# Add the tool to the collection
tools = [test_connection, search_items]

# Views
@csrf_exempt
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'query': openapi.Schema(
                type=openapi.TYPE_STRING,
            )
        },
        required=['query']
    )
)
@api_view(['POST'])
def query(request):
    query = request.data.get('query')

    try:
        # Initialize the agent
        agent = Agent(tools)
        
        # Ask the model and structure the response
        result = agent.ask(query)
        
        # Construct the response
        response_data = {
            'response': result
        }
        
        response = JsonResponse(response_data)
        
    except Exception as e:
        response_data = {'error': str(e)}
        response = JsonResponse(response_data, status=500)
 
    return response

@csrf_exempt
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'query': openapi.Schema(
                type=openapi.TYPE_STRING,
            )
        },
        required=['query']
    )
)
@api_view(['POST'])
def stream(request):
    query = request.data.get('query')
    
    return HttpResponse('Unimplemented')

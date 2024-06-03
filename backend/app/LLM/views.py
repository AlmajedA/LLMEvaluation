from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from langchain.tools import tool, BaseTool
from math import pi
from typing import Union

import os
import requests
import random

# LLMs
from .agent_gpt35 import AgentGPT35
from .agent_gpt4 import AgentGPT4
from .agent_llama import AgentLlama
from .agent_falcon import AgentFalcon

base_url = "http://localhost:8000" if os.environ.get('DEBUG') == "1" else os.environ.get('DEPLOY_URL')
global shopping_cart
shopping_cart = []

@tool
def test_connection() -> str:
    """Use this tool to test the connectivity. Mention the status code"""
    res = requests.get("https://google.com/")
    print("DEBUGGING IS:" + str(os.environ.get('DEBUG')))
    return f"Status code: {res.status_code}, the base url is: {base_url}"

@tool
def search_docs(search_query: str) -> list:
    """
    This Tool searches for documents given a search query which is anything that may lead to an answer to the query, \
        returns the top n_items matches.
    This should be your most used tool as it serves most cases.
    """

    res = requests.get(f"{base_url}/api/vector/similar_by_text/?query={search_query}&n={1}")
    print(res.json()['result'])
    return res.json()['result']

tools = [search_docs]

# Views

# GPT 3.5 Turbo
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
def query_gpt35(request):
    query = request.data.get('query')

    try:
        # Initialize the agent
        agent35 = AgentGPT35(tools)
        
        # Ask the model and structure the response
        result = agent35.ask(query)
        
        # Construct the response
        response_data = {
            'response': result
        }
        
        response = JsonResponse(response_data)
        
    except Exception as e:
        response_data = {'error': str(e)}
        response = JsonResponse(response_data, status=500)
 
    return response

# GPT 4
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
def query_gpt4(request):
    query = request.data.get('query')

    try:
        # Initialize the agent
        agent4 = AgentGPT4(tools)
        
        # Ask the model and structure the response
        result = agent4.ask(query)
        
        # Construct the response
        response_data = {
            'response': result
        }
        
        response = JsonResponse(response_data)
        
    except Exception as e:
        response_data = {'error': str(e)}
        response = JsonResponse(response_data, status=500)
 
    return response

# Llama-2-70b-chat 
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
def query_llama(request):
    query = request.data.get('query')

    try:
        # Initialize the agent
        agent_llama = AgentLlama(tools)
        
        # Ask the model and structure the response
        result = agent_llama.ask(query)
        
        # Construct the response
        response_data = {
            'response': result
        }
        
        response = JsonResponse(response_data)
        
    except Exception as e:
        response_data = {'error': str(e)}
        response = JsonResponse(response_data, status=500)
 
    return response

# Falcon-40b-instruct
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
def query_falcon(request):
    query = request.data.get('query')

    try:
        # Initialize the agent
        agent_falcon = AgentFalcon(tools)
        
        # Ask the model and structure the response
        result = agent_falcon.ask(query)
        
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

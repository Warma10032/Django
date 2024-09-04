# views.py
import requests
import gradio as gr
from django.shortcuts import render
from django.shortcuts import redirect
from fastapi import FastAPI
from django.http import HttpResponse
from django.core.handlers.asgi import ASGIHandler

def grodio_chat_view(request):
    return render(request, 'chat.html')


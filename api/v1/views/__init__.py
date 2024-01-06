#!/usr/bin/python3
"""import blueprint and create instance of blueprint"""
from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

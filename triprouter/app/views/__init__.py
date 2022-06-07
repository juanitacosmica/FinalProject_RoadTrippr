from flask import Blueprint

bp = Blueprint('index', __name__, url_prefix='/')
from .import index_view,login_view,navigation_view,questionaire_view,userinformation_view,userpage_view

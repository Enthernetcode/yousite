from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import YouTubeAccount, CommentFile #, #PaymentPlan
from . import db
import json

views = Blueprint('views', __name__)
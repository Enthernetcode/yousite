from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, YouTubeAccount, CommentFile #, #PaymentPlan
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from flask_security import recoverable

auth = Blueprint('auth', __name__)
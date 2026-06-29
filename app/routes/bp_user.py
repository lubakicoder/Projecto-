from flask import Blueprint, render_template, request, redirect, url_for 


bp_user = Blueprint('bp_user', __name__)

@bp_user.route('/')
def user_home():
    return render_template('index.html')

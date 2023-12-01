from flask import Flask, render_template, request, redirect, url_for, session
import os
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

app = Flask(__name__)
app.secret_key = b'secret_key'  # Change this to a secure secret key in production

# YouTube API setup
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def create_youtube_service():
    creds = None
    if 'token' in session:
        creds = session['token']

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)

        session['token'] = creds

    return build(API_SERVICE_NAME, API_VERSION, credentials=creds)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle signup logic here (e.g., store user data in a database)
        # For simplicity, we're using a session variable to store the username
        session['username'] = request.form['username']
        return redirect(url_for('dashboard'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic here (e.g., validate credentials against a database)
        # For simplicity, we're using a session variable to store the username
        session['username'] = request.form['username']
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    youtube_service = create_youtube_service()

    if request.method == 'POST':
        video_id = request.form['video_id']
        comment_text = request.form['comment_text']
        post_comment(youtube_service, video_id, comment_text)

    return render_template('dashboard.html')

def post_comment(youtube_service, video_id, comment_text):
    # Add logic to post comment using YouTube API
    # For simplicity, this example assumes the video_id is valid
    request = youtube_service.commentThreads().insert(
        part='snippet',
        body={
            'snippet': {
                'videoId': video_id,
                'topLevelComment': {
                    'snippet': {
                        'textOriginal': comment_text
                    }
                }
            }
        }
    )
    response = request.execute()
    print('Comment posted:', response)

if __name__ == '__main__':
    app.run(debug=True)

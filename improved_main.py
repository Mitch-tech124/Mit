from flask import Flask, Response, render_template, request, redirect, url_for, session, jsonify
import cv2
import os
from datetime import datetime
from functools import wraps
from cryptography.fernet import Fernet

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure the app with a secret key

# Initialize the video capture (0 for the first camera, or replace with video file path)
video_capture = cv2.VideoCapture(0)

# Background subtractor for motion detection
fgbg = cv2.createBackgroundSubtractorMOG2()

# Log file path
LOG_FILE = "motion_logs.txt"

# Generate a key for encrypting sensitive data
ENCRYPTION_KEY = Fernet.generate_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

def log_motion():
    """Log the motion detection event with a timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    encrypted_message = cipher_suite.encrypt(f"Motion detected at {timestamp}".encode())
    with open(LOG_FILE, "ab") as log:
        log.write(encrypted_message + b"\n")

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

motion_detected = False

def generate_frames():
    global motion_detected
    while True:
        # Read the frame from the video source
        success, frame = video_capture.read()
        if not success:
            break

        # Apply the background subtractor to detect motion
        fgmask = fgbg.apply(frame)

        # Highlight motion areas by drawing contours
        motion_detected = False
        contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) > 1000:  # Filter small movements
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                motion_detected = True

        if motion_detected:
            log_motion()

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame as part of an HTTP response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/motion_status')
@login_required
def motion_status():
    # Endpoint to check motion detection status
    return jsonify({'motion_detected': motion_detected})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Simple authentication (replace with a database for production)
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('index'))
        return "Invalid credentials. Try again."
    return """
    <style>
    body {
        font-family: Arial, sans-serif;
        text-align: center;
        margin-top: 10%;
        background-color: #f4f4f9;
    }
    form {
        display: inline-block;
        padding: 20px;
        background: #ffffff;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
    }
    input {
        margin: 10px 0;
        padding: 10px;
        width: 80%;
        border: 1px solid #ccc;
        border-radius: 5px;
    }
    button {
        padding: 10px 20px;
        background-color: #007BFF;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    button:hover {
        background-color: #0056b3;
    }
    </style>
    <form method="post">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>
    """

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    # Render the home page
    return """
    <style>
    body {
        font-family: Arial, sans-serif;
        text-align: center;
        margin-top: 5%;
        background-color: #f4f4f9;
    }
    h1 {
        color: #333;
    }
    a {
        display: block;
        margin: 20px 0;
        color: #007BFF;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    </style>
    <h1>Motion Detection Camera</h1>
    <img src='/video_feed' style='border: 2px solid #ccc; border-radius: 10px;'>
    <p><a href='/logout'>Logout</a></p>
    <script>
        setInterval(() => {
            fetch('/motion_status').then(response => response.json()).then(data => {
                if (data.motion_detected) {
                    alert('Motion detected!');
                }
            });
        }, 5000);
    </script>
    """

@app.route('/video_feed')
@login_required
def video_feed():
    # Route to serve the video stream
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

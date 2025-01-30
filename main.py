from flask import Flask, Response, render_template
import cv2

# Initialize Flask app
app = Flask(__name__)

# Initialize the video capture (0 for the first camera, or replace with video file path)
video_capture = cv2.VideoCapture(0)

# Background subtractor for motion detection
fgbg = cv2.createBackgroundSubtractorMOG2()

def generate_frames():
    while True:
        # Read the frame from the video source
        success, frame = video_capture.read()
        if not success:
            break

        # Apply the background subtractor to detect motion
        fgmask = fgbg.apply(frame)

        # Highlight motion areas by drawing contours
        contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) > 1000:  # Filter small movements
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame as part of an HTTP response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    # Render the home page
    return "<h1>Motion Detection Camera</h1><img src='/video_feed'>"

@app.route('/video_feed')
def video_feed():
    # Route to serve the video stream
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run()

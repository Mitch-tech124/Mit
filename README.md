

# Motion Detector Surveillance System

## Overview
This is a Flask-based motion detection surveillance system that uses OpenCV for real-time video processing. The system detects motion using a background subtractor and logs detected movements securely using encryption.

## Features
- **Live Video Streaming**: Access the video feed from a web interface.
- **Motion Detection**: Uses OpenCV's background subtraction to detect motion.
- **Secure Authentication**: Login system to prevent unauthorized access.
- **Encrypted Motion Logs**: Motion detection events are encrypted and stored securely.
- **Real-time Alerts**: The web interface provides alerts when motion is detected.

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Flask
- OpenCV
- Cryptography

### Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/motion-detector.git
   cd motion-detector
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open your browser and visit:
   ```
   http://localhost:5000
   ```

## Usage
- **Login**: Use `admin` as the username and `password` as the default credentials (change in production).
- **View Live Feed**: The home page displays the live video stream.
- **Logout**: Securely exit the session.

## Security Considerations
- **Update Credentials**: Change default login details for enhanced security.
- **Secure Logs**: Motion logs are encrypted using `cryptography.Fernet`.
- **HTTPS**: Deploy using HTTPS for better security.

## License
This project is licensed under the MIT License.

## Contributions
Feel free to contribute to this project by submitting pull requests or reporting issues.

## Contact
For any issues or suggestions, contact [mitchellofumejombo@gmail.com]


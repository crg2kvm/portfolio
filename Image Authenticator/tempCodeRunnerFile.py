from flask import Flask, request, render_template, session, redirect, url_for
from PIL import Image
import hashlib
import io
import sqlite3
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import cv2
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Check if a username already exists in the database
def username_exists(username):
    conn = sqlite3.connect('imagehashes.db')
    c = conn.cursor()
    c.execute('SELECT EXISTS(SELECT 1 FROM users WHERE username=? LIMIT 1)', (username,))
    exists = c.fetchone()[0]
    conn.close()
    return exists == 1

# Extract metadata from an image
def get_image_metadata(image_bytes):
    with Image.open(io.BytesIO(image_bytes)) as img:
        metadata = img.info
    return metadata

# Generate RSA keys (private and public)
def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem, public_pem

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Convert an image to a string representation of its pixels
def imageToString(image):
    im = Image.open(image, 'r')
    pixels = list(im.getdata())
    stringIMG = ""
    for i in pixels:
        for value in i:
            stringIMG += str(value)
    return stringIMG

# Convert a string representation of an image to a hash
def stringToHash(imgString):
    hash_function = hashlib.sha256()
    hash_function.update(imgString.encode())
    return hash_function.hexdigest()

# Set up the database and create tables if they do not exist
def setup_database():
    conn = sqlite3.connect('imagehashes.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT, 
            password TEXT,
            private_key TEXT,
            public_key TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_images (
            username TEXT,
            image_hash TEXT,
            photo_date TEXT,
            camera_model TEXT,
            ip_address TEXT,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    ''')
    conn.commit()
    conn.close()

setup_database()

# Save image metadata to the database
def save_image_with_metadata(username, image_hash, metadata, ip_address):
    photo_date = str(datetime.now().strftime("%D %H:%M:%S"))
    camera_model = metadata.get("camera_model")
    conn = sqlite3.connect('imagehashes.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO user_images (username, image_hash, photo_date, camera_model, ip_address) 
        VALUES (?, ?, ?, ?, ?)
    ''', (username, image_hash, photo_date, camera_model, ip_address))
    conn.commit()
    conn.close()

def save_image_with_metadata1(username, image_hash, metadata, ip_address):
    photo_date = str(datetime.now().strftime("%D %H:%M:%S"))
    camera_model = "Laptop"
    conn = sqlite3.connect('imagehashes.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO user_images (username, image_hash, photo_date, camera_model, ip_address) 
        VALUES (?, ?, ?, ?, ?)
    ''', (username, image_hash, photo_date, camera_model, ip_address))
    conn.commit()
    conn.close()

# Save image hash to the database with user information
def save_hash_to_db_with_user(username, image_hash):
    photo_date = str(datetime.now().strftime("%D %H:%M:%S"))
    camera_model = "None"
    ip_address = request.remote_addr
    conn = sqlite3.connect('imagehashes.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO user_images (username, image_hash, photo_date, camera_model, ip_address) 
        VALUES (?, ?, ?, ?, ?)
    ''', (username, image_hash, photo_date, camera_model, ip_address))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    logged_in = 'username' in session
    return render_template('index.html', logged_in=logged_in)

# Clear all image entries for a specific user
def clear_user_entries(username):
    conn = sqlite3.connect('imagehashes.db')
    c = conn.cursor()
    c.execute('DELETE FROM user_images WHERE username=?', (username,))
    conn.commit()
    conn.close()

@app.route('/clear_db')
def clear_my_entries():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    clear_user_entries(username)
    return 'Your entries have been cleared'

# Upload a photo and save its hash and metadata
def upload_photo(photo_path):
    with open(photo_path, 'rb') as file:
        image_bytes = file.read()
        imgString = imageToString(io.BytesIO(image_bytes))
        image_hash = stringToHash(imgString)
        metadata = get_image_metadata(image_bytes)
        ip_address = request.remote_addr

    if 'username' in session:
        username = session['username']
        save_image_with_metadata(username, image_hash, metadata, ip_address)
        return f"Photo hash: {image_hash} uploaded for user {username}"
    else:
        return "User not logged in"

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            imgString = imageToString(io.BytesIO(file.read()))
            image_hash = stringToHash(imgString)

            username = session['username']
            exists, _ = hash_exists_in_db(image_hash)
            if exists:
                return 'Hash is already in database'
            else:
                save_hash_to_db_with_user(username, image_hash)
                return 'Image hash: ' + image_hash
    return render_template('upload.html')

# Get all image hashes uploaded by a specific user
def get_hashes_by_user(username):
    conn = sqlite3.connect('imagehashes.db')
    c = conn.cursor()
    c.execute('SELECT image_hash, photo_date, camera_model, ip_address FROM user_images WHERE username=?', (username,))
    hashes = c.fetchall()
    conn.close()
    return hashes

# Check if an image hash already exists in the database
def hash_exists_in_db(image_hash):
    conn = sqlite3.connect('imagehashes.db')
    c = conn.cursor()
    c.execute('SELECT username FROM user_images WHERE image_hash=? LIMIT 1', (image_hash,))
    result = c.fetchone()
    conn.close()
    if result:
        username = result[0]
        return True, username
    else:
        return False, None

@app.route('/search', methods=['GET', 'POST'])
def search_hash():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            imgString = imageToString(io.BytesIO(file.read()))
            image_hash = stringToHash(imgString)
            exists, username = hash_exists_in_db(image_hash)
            if exists:
                message = f'Hash exists in database, uploaded by user: {username}'
            else:
                message = 'Hash does not exist in database'
            return message
    return render_template('search.html')

@app.route('/compare', methods=['GET','POST'])
def compare_images():
    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']

        if file1 and file2:
            imgString1 = imageToString(io.BytesIO(file1.read()))
            imgString2 = imageToString(io.BytesIO(file2.read()))

            hash1 = stringToHash(imgString1)
            hash2 = stringToHash(imgString2)

            if hash1 == hash2:
                return "The images have the same hash."
            else:
                return "The images have different hashes."
    return render_template('compare.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username_exists(username):
            return 'Username already exists. Please choose a different username.'

        hashed_password = generate_password_hash(password)

        private_key, public_key = generate_rsa_keys()

        conn = sqlite3.connect('imagehashes.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password, private_key, public_key) VALUES (?, ?, ?, ?)', 
                  (username, hashed_password, private_key, public_key))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('imagehashes.db')
        c = conn.cursor()
        c.execute('SELECT password FROM users WHERE username=?', (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[0], password):
            session['username'] = username
            return redirect(url_for('index'))

        return 'Invalid username or password'
    return render_template('login.html')

@app.route('/my_uploads')
def my_uploads():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    username = session['username']
    user_hashes = get_hashes_by_user(username)
    return render_template('my_uploads.html', user_hashes=user_hashes)


@app.route('/capture_and_upload')
def capture_and_upload():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    videoCaptureObject = cv2.VideoCapture(0)
    ret, frame = videoCaptureObject.read()
    videoCaptureObject.release()

    if ret:
        # Convert the captured frame to PIL Image
        img = Image.fromarray(frame)

        # Convert the Image to a string
        imgByteArr = io.BytesIO()
        img.save(imgByteArr, format='JPEG')
        imgByteArr = imgByteArr.getvalue()
        imgString = imageToString(io.BytesIO(imgByteArr))
        metadata = get_image_metadata(imgByteArr)
        print(metadata)
        ip_address = request.remote_addr
        #print("Here:",ip_address)
        # Generate hash
        image_hash = stringToHash(imgString)

        # Save hash to database
        username = session['username']
        save_image_with_metadata1(username, image_hash, metadata, ip_address)
        return 'Image captured and hash saved for user'
    else:
        return 'Failed to capture image'


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


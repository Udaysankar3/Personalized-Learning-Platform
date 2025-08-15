import requests
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
from flask_cors import CORS
from groq import Groq
import subprocess
import os
import uuid
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='1984',  # or your actual password
        database='learning_platform'
    )

    


app = Flask(__name__)
app.secret_key = '1984'  # Use a strong, random value in production


CORS(app)
app.config['UPLOAD_FOLDER'] = 'static/uploads'


client = Groq(api_key="")

# ---------- ROUTES for each HTML page ---------- #
from flask import flash

@app.route('/')
def home():
    return redirect(url_for('signup'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('signup'))

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))  # go to login after successful signup
        except mysql.connector.IntegrityError as e:
            if e.errno == 1062:
                flash('Username already exists.')
            else:
                flash('Something went wrong.')
            return redirect(url_for('signup'))

    return render_template('signup.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user is not None:
            return redirect(url_for('dashboard'))  # After successful login
        else:
            flash('Invalid username or password.')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')  # main dashboard page


@app.route('/logout')
def logout():
    # Optional: You can clear session data here if using sessions
    return redirect(url_for('signup'))  # Redirect to sign-up page

@app.route('/')
def index():
    return render_template('index.html')  # Your main dashboard page

@app.route('/text')
def text():
    return render_template('text.html')  # Digital Library

@app.route('/tested')
def tested():
    return render_template('tested.html')  # Assignments & Quizzes

@app.route('/courses')
def courses():
    return render_template('courses.html')  # All Courses

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(app.root_path, 'static/uploads'), filename)


# Route to handle profile photo upload
@app.route('/upload-photo', methods=['POST'])
def upload_photo():
    file = request.files['profile']
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'profile.jpg')  # static/uploads/profile.jpg
        file.save(filepath)
    return redirect(url_for('index'))

app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'POST':
        file = request.files['profile']
        if file:
            file.save(os.path.join('static/uploads', 'profile.jpg'))  # Save with fixed name
            return redirect(url_for('index'))
    return render_template('EditProfile.html')


@app.route('/course')
def course():
    return render_template('course.html')  # Course details

@app.route('/groq')
def groq():
    return render_template('Groq_Front.html')


@app.route('/book-preview')
def book_preview():
    preview_link = request.args.get('previewLink', '')
    return render_template('bookPreview.html', previewLink=preview_link)

@app.route('/quizzes')
def quizzes():
    subject = request.args.get('subject')
    week = request.args.get('week')
    return render_template("quizzes.html", subject=subject, week=week)


@app.route('/assessments')
def assessments():
    return render_template('assessments_quizzes.html')  # Quiz list page

@app.route('/compiler')
def compiler_ui():
    return render_template('compiler.html')


@app.route('/compile', methods=['POST'])
def compile_code():
    data = request.get_json()
    code = data.get('code')
    language = data.get('language')
    filename = f"temp_{uuid.uuid4().hex}"

    try:
        if language == "python":
            filepath = f"{filename}.py"
            with open(filepath, "w") as f:
                f.write(code)
            result = subprocess.check_output(["python", filepath], stderr=subprocess.STDOUT, timeout=5)

        elif language == "c":
            src = f"{filename}.c"
            exe = f"{filename}.exe"
            with open(src, "w") as f:
                f.write(code)
            subprocess.check_call(["gcc", src, "-o", exe])
            result = subprocess.check_output([exe], stderr=subprocess.STDOUT, timeout=5)

        elif language == "cpp":
            src = f"{filename}.cpp"
            exe = f"{filename}.exe"
            with open(src, "w") as f:
                f.write(code)
            subprocess.check_call(["g++", src, "-o", exe])
            result = subprocess.check_output([exe], stderr=subprocess.STDOUT, timeout=5)

        elif language == "java":
            import re
    # Extract class name
            match = re.search(r'public\s+class\s+(\w+)', code)
            if not match:
                return jsonify({"output": "Java class name not found or invalid."})
            class_name = match.group(1)
            src = f"{class_name}.java"
            with open(src, "w") as f:
             f.write(code)
            subprocess.check_call(["javac", src])
            result = subprocess.check_output(["java", class_name], stderr=subprocess.STDOUT, timeout=5)


        elif language == "javascript":
            filepath = f"{filename}.js"
            with open(filepath, "w") as f:
                f.write(code)
            result = subprocess.check_output(["node", filepath], stderr=subprocess.STDOUT, timeout=5)

        else:
            return jsonify({"output": "Unsupported language."})

        return jsonify({"output": result.decode("utf-8")})

    except subprocess.CalledProcessError as e:
        return jsonify({"output": e.output.decode("utf-8")})
    except subprocess.TimeoutExpired:
        return jsonify({"output": "Execution timed out."})
    except Exception as e:
        return jsonify({"output": f"Error: {str(e)}"})
    finally:
        for ext in [".py", ".c", ".cpp", ".exe", ".java", ".class", ".js"]:
            try:
                os.remove(filename + ext)
            except:
                pass

# ---------- BACKEND FUNCTIONAL ROUTES ---------- #

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']
    try:
        chat_completion = client.chat.completions.create(
            messages=[{ "role": "user", "content": user_input }],
            model="llama3-8b-8192",
        )
        response = chat_completion.choices[0].message.content
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)})


# @app.route('/compile', methods=['POST'])
# def compile_code():
#     data = request.get_json()
#     code = data.get('code')
#     language = data.get('language')

#     lang_map = {
#         "python": "python3",
#         "cpp": "cpp",
#         "c": "c",
#         "java": "java",
#         "javascript": "javascript"
#     }

#     lang = lang_map.get(language, "python3")

#     payload = {
#         "language": lang,
#         "source": code
#     }

#     response = requests.post("https://emkc.org/api/v2/piston/execute", json=payload)

#     if response.status_code == 200:
#         result = response.json()
#         return jsonify({"output": result.get("output")})
#     else:
#         return jsonify({"output": "Error executing code."}), 500


# ---------- MAIN ---------- #
if __name__ == '__main__':
    app.run(debug=True)

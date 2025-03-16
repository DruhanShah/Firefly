import os
import subprocess
import shutil
import tempfile
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

# Configuration (adjust as needed)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'py', 'txt', 'js', 'html', 'css', 'md'}
MAX_CONTENT_LENGTH = 1024 * 1024 * 1024

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if a file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def run_custom_code(directory_path):
    try:
        original_cwd = os.getcwd()
        os.chdir(directory_path)

        if not os.path.exists("main.py"):
            return None 

        process = subprocess.Popen(['python', 'main.py'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return_code = process.returncode

        stdout = stdout.decode('utf-8', errors='ignore') if stdout else ""
        stderr = stderr.decode('utf-8', errors='ignore') if stderr else ""

    except FileNotFoundError:
        return None
    except Exception as e:
        return None
    finally:
        os.chdir(original_cwd)
    return stdout, stderr, return_code


@app.route('/', methods=['GET', 'POST'])
def index():
    """Handles the main page with the directory input form."""
    if request.method == 'POST':
        if 'directory' not in request.files:
            return render_template('index.html', error='No directory part')

        directory = request.files['directory']

        if directory.filename == '':
            return render_template('index.html', error='No directory selected')
        temp_dir = tempfile.mkdtemp(dir=app.config['UPLOAD_FOLDER'])

        try:
            directory.save(os.path.join(temp_dir, directory.filename))
            shutil.unpack_archive(os.path.join(temp_dir, directory.filename), temp_dir)

            # Find the actual directory within the extracted files (if it's nested)
            extracted_dir = None
            for item in os.listdir(temp_dir):
                item_path = os.path.join(temp_dir, item)
                if os.path.isdir(item_path):
                    extracted_dir = item_path
                    break


            if extracted_dir is None:
                return render_template(
                    'index.html',
                    error='No directory found in archive.'
                )

            result = run_custom_code(extracted_dir)

            if result:
                stdout, stderr, return_code = result
                return render_template(
                    'result.html',
                    stdout=stdout,
                    stderr=stderr,
                    return_code=return_code
                )
            else:
                return render_template(
                    'index.html',
                    error='Error executing custom code. Check server logs.'
                )

        except Exception as e:
            print(f"An error occurred: {e}")
            return render_template('index.html', error=f'An error occurred: {e}')
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


    return render_template('index.html', error=None)


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/about')
def about():
    return render_template('about.html')


@app.errorhandler(413)
def request_entity_too_large(e):
    return render_template(
        'index.html',
        error='File size too large.  Maximum size is 16MB.'
    ), 413


if __name__ == '__main__':
    app.run(debug=True)

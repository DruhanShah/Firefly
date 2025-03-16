import os
import subprocess
import uuid
import shutil
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'zip', 'tar', 'gz', 'tgz', 'tar.gz'}  # Add more if needed
MAX_CONTENT_LENGTH = 1024 * 1024 * 1024  # 1 GiB
APP_ROOT = os.path.dirname(os.path.abspath(__file__))  # Project root

# Create directories if they don't exist
os.makedirs(os.path.join(APP_ROOT, UPLOAD_FOLDER), exist_ok=True)
os.makedirs(os.path.join(APP_ROOT, OUTPUT_FOLDER), exist_ok=True)

app.config['UPLOAD_FOLDER'] = os.path.join(APP_ROOT, UPLOAD_FOLDER)
app.config['OUTPUT_FOLDER'] = os.path.join(APP_ROOT, OUTPUT_FOLDER)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Error handling
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
app.config['TRAP_HTTP_EXCEPTIONS'] = True


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def run_main_script(process_type, input_dir, output_dir, documentation_dir=""):
    """
    Runs main.py with arguments based on the process type.
    Captures stdout and stderr. Handles errors.
    """
    try:
        command = ['python', 'main.py']  # Base command
        if process_type == 'documentation':
            command.extend(['--mode', 'documentation', '--input_dir', input_dir, '--output_dir', output_dir])
        elif process_type == 'code_generation':
            command.extend(['--mode', 'code_generation', '--documentation_dir', documentation_dir, '--output_dir', output_dir])
        else:
            return 1, "", "Error: Invalid process type."

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=APP_ROOT)
        stdout, stderr = process.communicate()

        return_code = process.returncode

        stdout_decoded = stdout.decode('utf-8', errors='ignore')
        stderr_decoded = stderr.decode('utf-8', errors='ignore')

        return return_code, stdout_decoded, stderr_decoded

    except FileNotFoundError:
        return 1, "", "Error: main.py not found in the application root directory."
    except Exception as e:
        return 1, "", f"An unexpected error occurred: {str(e)}"


def process_file(process_type, code_dir=None, documentation_dir=None):
    """Handles the common logic for both documentation and code generation."""
    unique_id = str(uuid.uuid4())
    output_dir = os.path.join(app.config['OUTPUT_FOLDER'], unique_id + "_output")
    os.makedirs(output_dir, exist_ok=True)

    try:
        return_code, stdout, stderr = run_main_script(process_type, code_dir, output_dir, documentation_dir)

        if return_code == 0:
            output_archive_path = os.path.join(
                app.config['OUTPUT_FOLDER'],
                f"{unique_id}_output.zip"
            )
            shutil.make_archive(os.path.join(
                app.config['OUTPUT_FOLDER'],
                f"{unique_id}_output"
            ), 'zip', output_dir)

            return render_template(
                'result.html',
                stderr=stderr,
                output_archive=f"{unique_id}_output.zip"
            )
        else:
            return render_template(
                'index.html',
                error=f"Error running main.py ({process_type}). Return code: {return_code}. Stderr: {stderr}. Stdout: {stdout}",
                process_type=process_type
            )


    except Exception as e:
        return render_template(
            'index.html',
            error=f"Error processing file: {str(e)}",
            process_type=process_type
        )
    finally:
        if code_dir:
            try:
                shutil.rmtree(code_dir)
            except FileNotFoundError:
                pass
            except Exception as e:
                print(f"Error during cleanup: {e}")
        if documentation_dir:
            try:
                shutil.rmtree(documentation_dir)
            except FileNotFoundError:
                pass
            except Exception as e:
                print(f"Error during cleanup: {e}")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        process_type = request.form.get('process_type')
        input_type = "code" if process_type == 'documentation' else "documentation"
        affix = "code" if process_type == 'documentation' else "docs"

        if f'{input_type}_archive' not in request.files:
            return render_template(
                'index.html',
                error=f'No {input_type} archive file part',
                process_type=process_type
            )

        code_archive = request.files[f'{input_type}_archive']

        if code_archive.filename == '':
            return render_template(
                'index.html',
                error=f'No {input_type} archive file selected',
                process_type=process_type
            )

        if code_archive and allowed_file(code_archive.filename):
            unique_id = str(uuid.uuid4())
            code_archive_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{affix}_" + secure_filename(code_archive.filename))
            code_archive.save(code_archive_path)

            code_dir = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{affix}")
            os.makedirs(code_dir, exist_ok=True)

            shutil.unpack_archive(code_archive_path, code_dir)
            os.remove(code_archive_path)

            return process_file(process_type, code_dir=code_dir)
        else:
            return render_template(
                'index.html',
                error='Invalid archive file type. Allowed types: ' + ', '.join(ALLOWED_EXTENSIONS),
                process_type=process_type
            )

    return render_template(
        'index.html',
        error=None,
        process_type=None
    )


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

@app.errorhandler(413)
def request_entity_too_large(e):
    return render_template(
        'index.html',
        error='File too large. Maximum size is 1 GiB.',
        process_type=request.form.get('process_type')
    ), 413


@app.errorhandler(500)
def internal_server_error(e):
    return render_template(
        'error.html',
        error="Internal Server Error.  Check the server logs."
    ), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        'error.html',
        error="Page Not Found."
    ), 404



if __name__ == '__main__':
    app.run(debug=True)

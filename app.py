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


def run_main_script(process_type, codebase_dir=None, output_dir="", examples_dir=None, docs_dir=None):
    """
    Runs main.py with arguments based on the process type.
    Captures stdout and stderr. Handles errors.
    """
    try:
        command = ['python', 'main.py']  # Base command
        if process_type == 'documentation':
            command.append('docs')
            command.extend(['--codebase_dir', codebase_dir, '--output_dir', output_dir])
        elif process_type == 'code_generation':
            command.append('code')
            command.extend(['--docs_dir', docs_dir, '--output_dir', output_dir])
            if examples_dir:
                command.extend(['--examples_dir', examples_dir])
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


def process_file(process_type, codebase_dir=None, output_dir=None, examples_dir=None, docs_dir=None):
    """Handles the common logic for both documentation and code generation."""
    unique_id = str(uuid.uuid4())
    output_dir = os.path.join(app.config['OUTPUT_FOLDER'], unique_id + "_output")
    os.makedirs(output_dir, exist_ok=True)

    try:
        return_code, stdout, stderr = run_main_script(process_type, codebase_dir, output_dir, examples_dir, docs_dir)

        if return_code == 0:
            output_archive_path = os.path.join(app.config['OUTPUT_FOLDER'], unique_id + "_output.zip")
            shutil.make_archive(os.path.join(app.config['OUTPUT_FOLDER'], unique_id + "_output"), 'zip', output_dir)

            return render_template('result.html',
                                   stderr=stderr,
                                   output_archive=unique_id + "_output.zip")
        else:
            return render_template('index.html', error=f"Error running main.py ({process_type}). Return code: {return_code}. Stderr: {stderr}. Stdout: {stdout}", process_type=process_type)


    except Exception as e:
        return render_template('index.html', error=f"Error processing file: {str(e)}", process_type=process_type)
    finally:
        # Cleanup
        for dir_path in [codebase_dir, examples_dir, docs_dir]:
            if dir_path:
                try:
                    shutil.rmtree(dir_path)
                except FileNotFoundError:
                    pass
                except Exception as e:
                    print(f"Error during cleanup: {e}")
        try:
            shutil.rmtree(output_dir) #clean up output, since we have archived it.
        except FileNotFoundError:
            pass #ALready removed.
        except Exception as e:
            print(f"Error during cleanup {e}")



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        process_type = request.form.get('process_type')

        if process_type == 'documentation':
            # Code Documentation
            if 'codebase_archive' not in request.files:
                return render_template('index.html', error='No codebase archive file part', process_type=process_type)

            codebase_archive = request.files['codebase_archive']

            if codebase_archive.filename == '':
                return render_template('index.html', error='No codebase archive file selected', process_type=process_type)

            if codebase_archive and allowed_file(codebase_archive.filename):
                unique_id = str(uuid.uuid4())
                codebase_archive_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_id + "_codebase_" + secure_filename(codebase_archive.filename))
                codebase_archive.save(codebase_archive_path)

                codebase_dir = os.path.join(app.config['UPLOAD_FOLDER'], unique_id + "_codebase")
                os.makedirs(codebase_dir, exist_ok=True)

                shutil.unpack_archive(codebase_archive_path, codebase_dir)
                os.remove(codebase_archive_path)

                return process_file(process_type, codebase_dir=codebase_dir)
            else:
                return render_template('index.html', error='Invalid codebase archive file type. Allowed types: ' + ', '.join(ALLOWED_EXTENSIONS), process_type=process_type)

        elif process_type == 'code_generation':
            # Code Generation

            if 'docs_archive' not in request.files:
                return render_template('index.html', error='No documentation archive file part', process_type=process_type)

            docs_archive = request.files['docs_archive']
            if docs_archive.filename == '':
                 return render_template('index.html', error='No documentation archive file selected', process_type=process_type)

            examples_archive = request.files.get('examples_archive') #Optional


            docs_dir = None
            examples_dir = None

            try:
                if docs_archive and docs_archive.filename != '' and allowed_file(docs_archive.filename):
                    unique_id = str(uuid.uuid4())
                    docs_archive_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_id + "_docs_" + secure_filename(docs_archive.filename))
                    docs_archive.save(docs_archive_path)

                    docs_dir = os.path.join(app.config['UPLOAD_FOLDER'], unique_id + "_docs")
                    os.makedirs(docs_dir, exist_ok=True)

                    shutil.unpack_archive(docs_archive_path, docs_dir)
                    os.remove(docs_archive_path)
                else:
                    return render_template('index.html', error='Invalid documentation archive file type. Allowed types: ' + ', '.join(ALLOWED_EXTENSIONS), process_type=process_type)


                if examples_archive and examples_archive.filename != '' and allowed_file(examples_archive.filename):
                    unique_id = str(uuid.uuid4())
                    examples_archive_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_id + "_examples_" + secure_filename(examples_archive.filename))
                    examples_archive.save(examples_archive_path)

                    examples_dir = os.path.join(app.config['UPLOAD_FOLDER'], unique_id + "_examples")
                    os.makedirs(examples_dir, exist_ok=True)

                    shutil.unpack_archive(examples_archive_path, examples_dir)
                    os.remove(examples_archive_path)


                return process_file(process_type, docs_dir=docs_dir, examples_dir=examples_dir)


            except Exception as e:
                return render_template('index.html', error=f"Error processing files: {str(e)}", process_type=process_type)

        else:
            return render_template('index.html', error='Invalid process type selected.', process_type=process_type)

    return render_template('index.html', error=None, process_type=None)


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

@app.errorhandler(413)
def request_entity_too_large(e):
    return render_template('index.html', error='File too large. Maximum size is 1 GiB.', process_type=request.form.get('process_type')), 413


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error="Internal Server Error.  Check the server logs."), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error="Page Not Found."), 404



if __name__ == '__main__':
    app.run(debug=True)

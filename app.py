"""
Flask app for the agent UI.
"""

import os
import json
import threading
import queue
import time
import subprocess
import uuid
import shutil
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
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

running_processes = {}

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
    """
    Handles the common logic for both documentation and code generation.
    """

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
                stdout=stdout,
                output_archive=f"{unique_id}_output.zip",
                output_id=unique_id
            )

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

@app.route('/list_files/<output_id>')
def list_files(output_id):
    """List files in the output directory."""
    output_dir = os.path.join(app.config['OUTPUT_FOLDER'], f"{output_id}_output")

    if not os.path.exists(output_dir):
        return jsonify({"error": "Output directory not found", "files": []}), 404

    files = []
    for root, _, filenames in os.walk(output_dir):
        for filename in filenames:
            rel_path = os.path.relpath(os.path.join(root, filename), output_dir)
            files.append(rel_path)

    return jsonify({"files": files})

@app.route('/view_file/<output_id>/<path:filename>')
def view_file(output_id, filename):
    """View a file's content."""
    output_dir = os.path.join(app.config['OUTPUT_FOLDER'], f"{output_id}_output")
    file_path = os.path.join(output_dir, filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return jsonify({"content": content})
    except UnicodeDecodeError:
        # Binary file
        return jsonify({"content": "Binary file cannot be displayed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def handle_process_io(process, input_queue, output_queue, execution_id):
    """Handle I/O for a running subprocess in a separate thread."""
    def read_output():
        while process.poll() is None:
            # Check for output from the process
            line = process.stdout.readline()
            if line:
                output_queue.put(line.decode('utf-8', errors='ignore'))

            # Check for input to send to the process
            try:
                if not input_queue.empty() and process.poll() is None:
                    input_text = input_queue.get_nowait()
                    process.stdin.write(input_text.encode('utf-8'))
                    process.stdin.flush()
            except Exception as e:
                output_queue.put(f"Error sending input: {str(e)}\n")

            time.sleep(0.1)

        # Read any remaining output after process completes
        remaining = process.stdout.read()
        if remaining:
            output_queue.put(remaining.decode('utf-8', errors='ignore'))

        # Mark process as completed
        running_processes[execution_id]['running'] = False

    thread = threading.Thread(target=read_output)
    thread.daemon = True
    thread.start()

@app.route('/run_code/<output_id>/<path:filename>', methods=['POST'])
def run_code(output_id, filename):
    """Run a Python file and set up I/O handling."""
    output_dir = os.path.join(app.config['OUTPUT_FOLDER'], f"{output_id}_output")
    file_path = os.path.join(output_dir, filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    if not filename.endswith('.py'):
        return jsonify({"error": "Only Python files can be executed"}), 400

    try:
        # Create a unique ID for this execution
        execution_id = str(uuid.uuid4())

        # Start the process
        process = subprocess.Popen(
            ['python', file_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=output_dir,
            bufsize=1,
            universal_newlines=False
        )

        # Set up queues for I/O
        input_queue = queue.Queue()
        output_queue = queue.Queue()

        # Store process info
        running_processes[execution_id] = {
            'process': process,
            'input_queue': input_queue,
            'output_queue': output_queue,
            'running': True
        }

        # Start I/O handler thread
        handle_process_io(process, input_queue, output_queue, execution_id)

        # Wait a bit to collect initial output
        time.sleep(0.5)

        # Get any initial output
        output = ""
        while not output_queue.empty():
            output += output_queue.get()

        return jsonify({
            "execution_id": execution_id,
            "output": output
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/check_output/<execution_id>')
def check_output(execution_id):
    """Check for new output from a running process."""
    if execution_id not in running_processes:
        return jsonify({"error": "Execution not found"}), 404

    process_data = running_processes[execution_id]
    output = ""

    while not process_data['output_queue'].empty():
        output += process_data['output_queue'].get()

    return jsonify({
        "output": output,
        "running": process_data['running']
    })

@app.route('/send_input/<execution_id>', methods=['POST'])
def send_input(execution_id):
    """Send input to a running process."""
    if execution_id not in running_processes:
        return jsonify({"error": "Execution not found"}), 404

    process_data = running_processes[execution_id]

    if not process_data['running']:
        return jsonify({"error": "Process is not running"}), 400

    try:
        input_data = request.json.get('input', '')
        process_data['input_queue'].put(input_data)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stop_execution/<execution_id>', methods=['POST'])
def stop_execution(execution_id):
    """Stop a running process."""
    if execution_id not in running_processes:
        return jsonify({"error": "Execution not found"}), 404

    process_data = running_processes[execution_id]

    if not process_data['running']:
        return jsonify({"error": "Process is not running"}), 400

    try:
        process_data['process'].terminate()
        process_data['running'] = False
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

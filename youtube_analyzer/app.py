from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
import subprocess

app = Flask(__name__)
app.secret_key = "supersecretkey"  # For flashing messages

# Set upload and processed folders
UPLOAD_FOLDER = 'uploads/'
PROCESSED_FOLDER = 'processed/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and file.filename == 'watch-history.json':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Path to the processing Python script
        script_path = '../data_preprocessing.py'  # Path to your Python script
        processed_file_path = os.path.join(app.config['PROCESSED_FOLDER'], 'watch_history_processed.csv')

        try:
            # Run the Python script with the uploaded file as input
            result = subprocess.run(['python', script_path, file_path, processed_file_path],
                                    capture_output=True, text=True)

            print(result.stdout)  # Print the output for debugging
            print(result.stderr)  # Print any error messages for debugging

            # Check if the processed file exists
            if os.path.exists(processed_file_path):
                # Generate a download URL
                download_url = url_for('download_processed_file', filename='watch_history_processed.csv')
                return {'message': 'File processed successfully', 'download_url': download_url}

            else:
                flash('Processed file not found')
                return redirect(url_for('index'))

        except Exception as e:
            flash(f'Error processing file: {e}')
            return redirect(request.url)

    else:
        flash('Only watch-history.json files are allowed')
        return redirect(request.url)

@app.route('/processed/<filename>')
def download_processed_file(filename):
    return send_file(os.path.join(app.config['PROCESSED_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

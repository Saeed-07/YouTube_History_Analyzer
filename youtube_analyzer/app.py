from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
import os
import subprocess

app = Flask(__name__)

# Set upload and processed folders
UPLOAD_FOLDER = 'uploads/'
PROCESSED_FOLDER = 'processed/'
EDA_FOLDER = 'static/eda_plots/'

# Create folders if they don't exist
for folder in [UPLOAD_FOLDER, PROCESSED_FOLDER, EDA_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['EDA_FOLDER'] = EDA_FOLDER

# Required plot files for EDA
REQUIRED_PLOTS = [
    'top_watched_channels.png', 'top_watched_videos.png', 'views_by_day.png', 
    'views_by_hour.png', 'views_by_month.png', 'views_by_year.png', 
    'watchtime_per_day.png', 'watchtime_per_hour.png'
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file and file.filename == 'watch-history.json':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Path to the processing Python script
        script_path = '../data_preprocessing.py'  # Adjust path as necessary
        processed_file_path = os.path.join(app.config['PROCESSED_FOLDER'], 'watch_history_processed.csv')

        try:
            # Step 1: Run the preprocessing script
            result = subprocess.run(['python', script_path, file_path, processed_file_path],
                                    capture_output=True, text=True)

            if os.path.exists(processed_file_path):
                # Step 2: Run the EDA script
                eda_script_path = '../data_eda.py'  # Adjust path as necessary
                eda_output_folder = app.config['EDA_FOLDER']
                if not os.path.exists(eda_output_folder):
                    os.makedirs(eda_output_folder)

                eda_result = subprocess.run(['python', eda_script_path, processed_file_path, eda_output_folder],
                                            capture_output=True, text=True)

                # Check if all required EDA charts were generated
                eda_output_files = os.listdir(eda_output_folder)
                missing_plots = [plot for plot in REQUIRED_PLOTS if plot not in eda_output_files]

                if not missing_plots:
                    return jsonify({
                        'message': 'File processed and EDA completed successfully',
                        'download_url': url_for('download_processed_file', filename='watch_history_processed.csv'),
                        'eda_plots_url': url_for('show_eda_plots')
                    })
                else:
                    return redirect(url_for('index'))

            else:
                return redirect(url_for('index'))

        except Exception as e:
            return redirect(request.url)

    else:
        return redirect(request.url)

@app.route('/eda_plots')
def show_eda_plots():
    # Fetch the list of plot image files
    eda_output_folder = app.config['EDA_FOLDER']
    plot_files = [f for f in os.listdir(eda_output_folder) if os.path.isfile(os.path.join(eda_output_folder, f))]
    
    # Ensure specific plots are present (from your request)
    available_plots = [f for f in REQUIRED_PLOTS if f in plot_files]

    if available_plots:
        return render_template('eda_plots.html', plot_files=available_plots)
    else:
        return redirect(url_for('index'))

@app.route('/processed/<filename>')
def download_processed_file(filename):
    return send_file(os.path.join(app.config['PROCESSED_FOLDER'], filename), as_attachment=True)

@app.route('/eda/<filename>')
def download_eda_output(filename):
    return send_file(os.path.join(app.config['EDA_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

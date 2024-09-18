# YouTube Watch History Analyzer

A web application to analyze and visualize your YouTube watch history. This tool helps you understand your viewing habits by processing your YouTube history data and generating insightful visualizations.

## Features

- **Upload YouTube Watch History**: Upload your YouTube watch history JSON file to the application.
- **Data Processing**: The tool processes the uploaded file to extract relevant information.
- **Exploratory Data Analysis (EDA)**: Generate various charts and visualizations based on your watch history data.
- **Sample Dashboard**: View a sample Tableau dashboard to understand the type of insights you can generate with your data.
- **Download Processed Data**: Download the processed data file for further analysis.

## Getting Started

### Prerequisites

- Python 3.7 or later
- Flask
- Required Python libraries: Flask, pandas, numpy, matplotlib, seaborn (install using `pip install -r requirements.txt`)

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Saeed-07/YouTube_History_Analyzer
   cd YouTube_History_Analyzer
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up the Environment:**
   - Create an `.env` file in the root directory and add necessary environment variables (if applicable).

### Running the Application

1. **Start the Flask Server:**
   ```bash
   python app.py
   ```

2. **Access the Application:**
   Open your web browser and navigate to `http://localhost:5000`.

### How to Use

1. **Upload Your Data:**
   - Go to the home page of the application.
   - Click on the "Upload" button and select your `watch-history.json` file.

2. **View EDA Results:**
   - After processing, you will see various visualizations and insights about your watch history.
   - A sample Tableau dashboard link will be provided to show the type of insights that can be generated.

3. **Download Processed Data:**
   - A link to download the processed data will be available after the data is processed.

### Sample Dashboard

To get a preview of the type of insights you can generate with your data, visit the sample Tableau dashboard:

[View Sample Dashboard](https://public.tableau.com/views/YoutubeWatchHistoryAnalyzer/Dashboard1)

### Contributing

Feel free to fork the repository and submit pull requests. If you encounter any issues or have suggestions, please open an issue on GitHub.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
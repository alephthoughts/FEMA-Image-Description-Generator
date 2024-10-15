# FEMA Image Description Generator

This application processes images in a specified folder, generates descriptions for FEMA using OpenAI's GPT-4o Vision model, and provides an Excel file with the results.

## Features

- Supports various image formats including JPEG, PNG, GIF, BMP, TIFF, and HEIC
- Processes images in batches, with a 2-second break after every 10 images
- Generates detailed descriptions focused on disaster assessment and response
- Provides a user-friendly Streamlit interface
- Outputs results in an downloadable Excel file

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/fema-image-description-generator.git
   cd fema-image-description-generator
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. In the web interface:
   - Enter your OpenAI API key
   - Provide the folder path containing the images
   - Click "Process Images" to start the analysis
   - Once processing is complete, download the Excel file with the results

## Files

- `app.py`: The main Streamlit application
- `backend.py`: Contains the core functionality for image processing and API interaction
- `requirements.txt`: Lists all the Python packages required for this project

## Note

Ensure you have the necessary permissions to access the specified folder path and that your OpenAI API key has sufficient credits for the number of images you plan to process.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

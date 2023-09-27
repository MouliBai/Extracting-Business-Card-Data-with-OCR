# Business Card Information Extraction and Management Application

This Streamlit application allows users to upload an image of a business card and extract relevant information from it using easyOCR. The extracted information includes the company name, card holder name, designation, mobile number, email address, website URL, area, city, state, and pin code. Users can also save the extracted information along with the uploaded business card image into a database, and have the ability to read, update, and delete data through the Streamlit user interface.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your system.
- [Streamlit](https://streamlit.io/) installed. You can install it using `pip`:
  ```
  pip install streamlit
  ```
- [easyOCR](https://github.com/JaidedAI/EasyOCR) installed. You can install it using `pip`:
  ```
  pip install easyocr
  ```
- A database management system like [SQLite](https://www.sqlite.org/) or [MySQL](https://www.mysql.com/) installed, and appropriate Python packages for database interaction (e.g., `sqlite3`, `mysql-connector-python`).

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/MouliBai/Extracting-Business-Card-Data-with-OCR.git
   ```
2. Change the directory to the project folder:
   ```
   cd Extracting-Business-Card-Data-with-OCR
   ```
3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit application:
   ```
   streamlit run app.py
   ```

2. The application will open in your web browser.

3. Follow the on-screen instructions to upload a business card image and extract information.

4. You can save the extracted information to the database and manage it using the provided options.

## Features

- Upload a business card image and extract information such as company name, cardholder name, designation, mobile number, email address, website URL, area, city, state, and pin code.
- Save extracted information along with the uploaded image to a database.
- Read, update, and delete data from the database through the Streamlit UI.
- User-friendly interface for easy interaction.
- Scalable and maintainable architecture.

## Project Structure

The project structure is organized as follows:

- `app.py`: The main Streamlit application file containing the GUI and application logic.
- `Creative Modern Business Card.zip`: Sample input for the project
- `requirements.txt`: List of Python packages required for the project.
- `README.md`: This readme file.

## Contributing

Contributions are welcome! Feel free to open issues and pull requests to improve this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

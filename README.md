# PDF Extractor

PDF Extractor is a web application that allows users to upload PDF files and extract their text content using the Moonshot API. It provides an easy-to-use interface for managing and viewing the uploaded files and their extracted content.

## Features

- Upload PDF files for text extraction
- List uploaded files with their status
- Delete uploaded files
- View file information and extracted text content
- Secure storage of Moonshot API key using browser's local storage

## Getting Started

### Prerequisites

- A modern web browser (Chrome, Firefox, Safari, Edge)
- A Moonshot API key (obtain from [https://platform.moonshot.cn/](https://platform.moonshot.cn/))

### Installation

1. Make sure you have Python installed on your system. If not, you can download and install it from the official Python website: [https://www.python.org](https://www.python.org)

2. Clone the repository: 

```
git clone https://github.com/temberature/pdf-extractor.git
```

3. Navigate to the project directory:

```
cd pdf-extractor
```

4. Install the required dependencies using pip:

```
pip install -r requirements.txt
```

This command will install all the necessary packages listed in the `requirements.txt` file, including Flask, openai, and Gunicorn.

5. You're now ready to run the application!

### Usage

0. Start the application using Gunicorn:

```
gunicorn app:app
```

1. Enter your Moonshot API key in the provided input field and click "保存" (Save).
2. Click the "选择PDF文件" (Choose PDF File) button to select a PDF file from your local machine.
3. Click the "上传文件" (Upload File) button to upload the selected file for text extraction.
4. The uploaded files will be listed in the "已上传的文件" (Uploaded Files) section.
5. Use the action buttons next to each file to delete the file, view file information, or view the extracted text content.

## Backend Setup

The PDF Extractor project requires a backend server to handle file uploads, text extraction, and file management. The backend server should expose the following API endpoints:

- `POST /extract`: Upload a PDF file and initiate text extraction.
- `GET /files`: List all uploaded files.
- `GET /files/{file_id}`: Get information about a specific file.
- `DELETE /files/{file_id}`: Delete a specific file.
- `GET /files/{file_id}/content`: Get the extracted text content of a specific file.

Ensure that the backend server is properly configured with the Moonshot API credentials and follows the necessary security practices.

## Contributing

Contributions to the PDF Extractor project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [Moonshot API](https://platform.moonshot.cn/) for providing the text extraction service.
- [Font Awesome](https://fontawesome.com/) for the icons used in the user interface.
- [jQuery](https://jquery.com/) for simplifying DOM manipulation and AJAX requests.
- [接入Kimichat的API，免费抽取PDF文本](https://mp.weixin.qq.com/s/BkIfl_RLnBO_NnF4I0ylmA)
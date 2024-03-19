from flask import Flask, render_template, request, jsonify
from pathlib import Path
from openai import OpenAI
import time
import os
import tempfile

app = Flask(__name__)

# 从环境变量获取API密钥 
api_key = os.environ.get('MOONSHOT_API_KEY')
client = OpenAI(
    api_key=api_key,
    base_url="https://api.moonshot.cn/v1",
)

from logging.config import dictConfig

# 配置日志记录
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/files', methods=['GET'])
def list_files():
    try:
        file_list = client.files.list()
        
        # 将 FileObject 转换为字典
        files_data = []
        for file in file_list.data:
            file_data = {
                'id': file.id,
                'filename': file.filename,
                'bytes': file.bytes,
                'created_at': file.created_at,
                'status': file.status,
                'status_details': file.status_details
            }
            files_data.append(file_data)
        
        return jsonify({"files": files_data})
    except Exception as e:
        app.logger.error(f"Error listing files: {str(e)}")
        return jsonify({"error": "Error listing files"}), 500

@app.route('/files/<string:file_id>', methods=['GET'])
def get_file(file_id):
    try:
        file = client.files.retrieve(file_id=file_id)
        
        # 将 FileObject 转换为字典
        file_data = {
            'id': file.id,
            'filename': file.filename,
            'bytes': file.bytes,
            'created_at': file.created_at,
            'status': file.status,
            'status_details': file.status_details
        }
        
        return jsonify(file_data)
    except Exception as e:
        app.logger.error(f"Error retrieving file info: {str(e)}")
        return jsonify({"error": "Error retrieving file info"}), 500

@app.route('/files/<string:file_id>', methods=['DELETE'])
def delete_file(file_id):
    try:
        client.files.delete(file_id=file_id)
        return jsonify({"message": "File deleted successfully"})
    except Exception as e:
        app.logger.error(f"Error deleting file: {str(e)}")
        return jsonify({"error": "Error deleting file"}), 500

@app.route('/extract', methods=['POST'])
def extract():
    # 获取上传的文件
    pdf_file = request.files['pdf_file']
    
    # 记录文件名和大小
    app.logger.info(f"Received file: {pdf_file.filename}, size: {pdf_file.content_length} bytes")
    
    try:
        # 从原始文件名中提取文件名和扩展名
        file_name, file_ext = os.path.splitext(pdf_file.filename)
        
        # 将FileStorage对象转换为临时文件对象,使用原始文件名
        with tempfile.NamedTemporaryFile(delete=False, prefix=file_name, suffix=file_ext) as tmp_file:
            pdf_file.save(tmp_file.name)
            tmp_file.flush()

            # 记录临时文件的路径
            app.logger.info(f"Saved to temporary file: {tmp_file.name}")

            # 上传PDF文件
            file_object = client.files.create(file=open(tmp_file.name, "rb"), purpose="file-extract")

        # 等待文件处理完成
        while file_object.status != 'ok':         
            file_object = client.files.retrieve(file_id=file_object.id)
            if file_object.status_details == 'error':
                app.logger.error(f"File processing failed: {file_object.status_details}")
                return jsonify({"error": "文件处理失败"}), 500
            time.sleep(1)  # 等待1秒更新进度
        
        # 获取文件内容
        file_content = client.files.content(file_id=file_object.id).text
        
        app.logger.info(f"File content extracted, length: {len(file_content)} characters")
        
        return jsonify({"text": file_content})

    except openai.error.InvalidRequestError as e:
        app.logger.error(f"InvalidRequestError: {str(e)}")
        return jsonify({"error": "Invalid request. The file might be corrupted or in an unsupported format."}), 400
    except openai.error.InternalServerError as e:
        app.logger.error(f"InternalServerError: {str(e)}")
        return jsonify({"error": "Server error. The file extraction service is currently unavailable."}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "Unknown error occurred during file extraction."}), 500
    
    finally:
        # 删除临时文件
        os.unlink(tmp_file.name)

@app.route('/files/<string:file_id>/content', methods=['GET'])
def get_file_content(file_id):
    try:
        file_content = client.files.content(file_id=file_id).text
        return jsonify({"content": file_content})
    except Exception as e:
        app.logger.error(f"Error retrieving file content: {str(e)}")
        return jsonify({"error": "Error retrieving file content"}), 500
        
if __name__ == '__main__':
    app.run()
from flask import Flask, render_template, request, jsonify
from pathlib import Path
from openai import OpenAI
import time
import os

app = Flask(__name__)

# 从环境变量获取API密钥 
api_key = os.environ.get('MOONSHOT_API_KEY')
client = OpenAI(
    api_key=api_key,
    base_url="https://api.moonshot.cn/v1",
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    # 获取上传的文件
    pdf_file = request.files['pdf_file']
    
    try:
        # 上传PDF文件
        file_object = client.files.create(file=pdf_file, purpose="file-extract")

        # 等待文件处理完成
        while file_object.status != 'ok':         
            file_object = client.files.retrieve(file_id=file_object.id)
            if file_object.status_details == 'error':
                return jsonify({"error": "文件处理失败"})
            time.sleep(1)  # 等待1秒更新进度
        
        # 获取文件内容
        file_content = client.files.content(file_id=file_object.id).text
        
        return jsonify({"text": file_content})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run()
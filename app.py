from flask import Flask, request, send_file, jsonify
import gdown
import os
import zipfile
import uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = "./downloads"

# ensure dir exists
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/download-and-zip', methods=['GET'])
def download_and_zip():
    try:
        folder_url = request.args.get('folder_url')
        if not folder_url:
            return jsonify({"error": "folder_url parameter is required"}), 400

        folder_id = str(uuid.uuid4())
        download_path = os.path.join(DOWNLOAD_FOLDER, f"{folder_id}")
        zip_path = os.path.join(DOWNLOAD_FOLDER, f"{folder_id}.zip")

        os.makedirs(download_path, exist_ok=True)
        gdown.download_folder(folder_url, output=download_path, quiet=False)

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(download_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, download_path)
                    zipf.write(file_path, arcname)
        return send_file(zip_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)

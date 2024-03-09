from flask import Flask, request, send_file
from flask_restful import Api, Resource
import os

app = Flask(__name__)
api = Api(app)

# Specify the folder where uploaded files will be stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DELETE_FOLDER = 'uploads'
app.config['DELETE_FOLDER'] = DELETE_FOLDER


class ResumeUpload(Resource):
    def post(self):
        # Check if the request contains files
        if 'files[]' not in request.files:
            return {'error': 'No files part'}, 400

        files = request.files.getlist('files[]')

        # Iterate over the uploaded files
        uploaded_files = []
        for file in files:
            # If the user does not select a file, the browser submits an empty part
            if file.filename == '':
                return {'error': 'No selected file'}, 400

            # Save the uploaded file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            uploaded_files.append(file_path)

        return {'message': 'Files uploaded successfully', 'file_paths': uploaded_files}



class ResumeDownload(Resource):
    def get(self, filename):
        # Construct the file path
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Check if the file exists
        if not os.path.exists(file_path):
            return {'error': 'File not found'}, 404

        # Return the file for download
        return send_file(file_path, as_attachment=True)

class ExistingFileDelete(Resource):
    def delete(self):
        # Get the list of files in the folder
        folder_path = app.config['DELETE_FOLDER']
        files = os.listdir(folder_path)

        # Delete all files in the folder
        deleted_files = []
        for file in files:
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)
            deleted_files.append(file)

        return {'message': 'All files deleted successfully', 'deleted_files': deleted_files}



# Create API routes
api.add_resource(ResumeUpload, '/resumeUpload')
api.add_resource(ResumeDownload, '/resumeDownload/<string:filename>')
api.add_resource(ExistingFileDelete, '/existingFileDelete')

if __name__ == '__main__':
    # Create the 'uploads' folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    app.run(debug=True)

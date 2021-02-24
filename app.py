"""
TODO:
- Properly configure app for deployment
- Fix any security shit with file paths
- Periodically remove files from uploads and downloads (without annoying users)

- Allow numerous uploads in html
- CSS shit

- Could maybe encrypt PDF's ?

- maybe write a test/build script that includes something like this:
    find -name "*.pdf" -exec rm {} \;
    BUT with a directory specified so you don't accidentally delete all your PDF's on your computer

Lot's of help from here:
https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
"""
import os
import secrets

from flask import Flask, render_template, request, redirect, flash, send_file
from werkzeug.utils import secure_filename
from pdf_operations import merge_pdfs

DOWNLOAD_FOLDER = '/home/tom/Desktop/Github/PDF_Website/downloads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
app.config['UPLOAD_FOLDER'] = '/home/tom/Desktop/Github/PDF_Website/uploads'
app.config['MAX_CONTENT_PATH'] = 2000000


@app.route('/')
def home():
    return render_template('home.jinja2')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/merging_page', methods=["GET", "POST"])
def merging_page():
    if request.method == 'POST':
        all_file_objects = request.files
        if '' in all_file_objects:
            flash('Empty filename given')
            return redirect(request.url)

        file_paths = []
        for file in all_file_objects.values():
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file_paths.append(file_location)
                file.save(file_location)

        merged_pdf_path = os.path.join(DOWNLOAD_FOLDER, "combined.pdf")  # security issue?
        merge_pdfs(file_paths, merged_pdf_path)

        return send_file("downloads/combined.pdf", as_attachment=True)

    else:
        return render_template('merging_page.jinja2')


if __name__ == '__main__':
    app.run()

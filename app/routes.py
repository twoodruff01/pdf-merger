import os
import secrets
from flask import render_template, redirect, request, flash, send_file
from werkzeug.utils import secure_filename

from app import app
from utils.pdf_operations import merge_pdfs

DOWNLOAD_FOLDER = '/home/tom/Desktop/Github/PDF_Website/loads/downloads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
app.config['UPLOAD_FOLDER'] = '/home/tom/Desktop/Github/PDF_Website/loads/uploads'
app.config['MAX_CONTENT_PATH'] = 2000000


@app.route('/')
@app.route('/home')
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

        return send_file(merged_pdf_path, as_attachment=True)  # this path needs fixing

    else:
        return render_template('merging_page.jinja2')

import os
from flask import send_file
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import current_app
from werkzeug.utils import secure_filename

from .utils.pdf_operations import merge_pdfs


COMBINED_FILE_NAME = "combined.pdf"
bp = Blueprint('merging', __name__)


@bp.route('/merging_page', methods=["GET", "POST"])
def merging_page():
    current_app.logger.info('User accessing merging_page')
    if request.method == 'POST':
        current_app.logger.info('User submitted file(s)')
        all_file_objects = request.files
        if '' in all_file_objects:
            flash('Empty filename given')
            return redirect(request.url)

        # Save all files into a list, with security checks
        file_paths = []
        for file in all_file_objects.values():
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_location = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file_paths.append(file_location)
                file.save(file_location)
            if file and not allowed_file(file.filename):
                current_app.logger.warning("User submitted dodgy filename")

        # Perform merge operation and send combined file to user
        merged_pdf_path = os.path.join(current_app.config['DOWNLOAD_FOLDER'], COMBINED_FILE_NAME)
        merge_pdfs(file_paths, merged_pdf_path)
        return send_file(merged_pdf_path, as_attachment=True)

    else:
        return render_template('merging_page.jinja2')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

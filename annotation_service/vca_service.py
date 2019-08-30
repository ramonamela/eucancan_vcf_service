from flask import Flask, request, Response
from werkzeug.utils import secure_filename
from os.path import exists

app = Flask(__name__)

vcf_folder = "/mnt/nfs/stored_vcfs/"


@app.route("/files/", methods=["POST"])
@app.route("/files/<file_name>", methods=["POST"])
def upload_file(filename=None):
    f = request.files["vcf_file"]

    if filename is None:
        filename = f.filename
    secure_name = secure_filename(filename)
    # Empty filename
    if not secure_name:
        return "Malformed or empty file name\n", 422
    full_path = "{}{}".format(vcf_folder, secure_name)
    # Verify extension
    if not secure_name.lower().endsWith(".vcf.gz"):
        return "Unsupported file extension", 415

    full_path = "{}{}".format(vcf_folder, secure_name)
    # File already exists
    if exists(full_path):
        return "File already exists\n", 409  # Response(status=409)
    else:
        try:
            f.save(full_path)
        except Exception as e:
            print(e)
            return "Error storing the file\n", 500
        return Response(status=200)

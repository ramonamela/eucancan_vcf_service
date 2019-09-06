from flask import Flask, request, Response, send_from_directory, abort
from werkzeug.utils import secure_filename
from os.path import exists
from os import remove
from json import loads

app = Flask(__name__)

vcf_folder = "/mnt/nfs/stored_vcfs/"


@app.route("/files/", methods=["POST"])
def vcf_annotation_bridge():
    try:
        f = request.files["vcf_file"]
    except KeyError:
        return "vcf file not found\n", 400
    return vcf_annotation(f.filename)

@app.route("/files/<filename>", methods=["GET","POST","DELETE"])
def vcf_annotation(filename):
    secure_name = secure_filename(filename)
    if request.method == "POST":
        try:
            f = request.files["vcf_file"]
        except KeyError:
            return "vcf file not found\n", 400

        # Empty filename
        if not secure_name:
            return "Malformed or empty file name\n", 422

        # Verify extension
        if not secure_name.lower().endswith(".vcf.gz"):
            return "Unsupported file extension\n", 415

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
    elif request.method == "DELETE":
        if filename is None or not secure_name:
            return "Malformed or empty file name\n", 422
        full_path = "{}{}".format(vcf_folder, secure_name)
        print("Try to delete {}".format(full_path))
        if exists(full_path):
            remove(full_path)
            return Response(status=200)
        return Response(status=500)
    elif request.method == "GET":
        try:
            return send_from_directory(vcf_folder,
                                       filename=filename, as_attachment=False)
        except FileNotFoundError:
            abort(404)
    elif request.method == "PUT":
        trans_props = loads(request.data)
        print(trans_props)


if __name__ == '__main__':
    app.env="development"
    app.run(debug=False, host="0.0.0.0", port=5000)

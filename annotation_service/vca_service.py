from flask import Flask, request, Response
from werkzeug.utils import secure_filename
from os.path import exists
from os import remove

app = Flask(__name__)

vcf_folder = "/mnt/nfs/stored_vcfs/"


@app.route("/files/", methods=["POST","DELETE"])
@app.route("/files/<filename>", methods=["POST","DELETE"])
def vcf_annotation(filename=None):
    secure_name = secure_filename(filename)
    if request.method == "POST":
        f = request.files["vcf_file"]

        if filename is None:
            filename = f.filename

        # Empty filename
        if not secure_name:
            return "Malformed or empty file name\n", 422
        full_path = "{}{}".format(vcf_folder, secure_name)
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




if __name__ == '__main__':
    app.env="development"
    app.run(debug=False, host="0.0.0.0", port=5000)

#https://medium.com/customorchestrator/simple-reverse-proxy-server-using-flask-936087ce0afb
#https://stackoverflow.com/questions/6656363/proxying-to-another-web-service-with-flask

from flask import Flask,request,redirect,Response
import requests
import argparse
import sys

app = Flask(__name__)
SITE_NAME = "http://localhost:8000"

input_port = None
service_port = None
service_address = None

@app.route('/')
def joke():
    return 'Flask is running as internal proxy!'

@app.route('/<path:path>',methods=['PUT','GET','POST','DELETE'])
def proxy(path):
    import sys
    if request.method=='GET':
        resp = requests.get("%s%s" % (SITE_NAME, path))
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response
    elif request.method=='POST':
        ## THIS STEP IS SPECIFIC FOR THIS APPLICATION. TO DO IT IN A GENERAL WAY, ITERATE THROUGH THE FILES
        try:
            f = request.files["vcf_file"]
        except Exception:
            return "vcf file not found\n", 422

        file_to_forward = {"vcf_file": (f.filename, f.stream, f.mimetype)}
        resp = requests.post("%s%s" % (SITE_NAME, path),
                             files=file_to_forward)

        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response
    elif request.method=='DELETE':
        resp = requests.delete("%s%s" % (SITE_NAME, path))
        excluded_headers = ['content-encoding', 'content-length',
                            'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response
    elif request.method=='PUT':
        file_to_forward = {}
        for key in list(request.files.keys()):
            file_to_forward[key] = request.files[key]
        resp = requests.put("%s%s" % (SITE_NAME, path), data=request.data, files=file_to_forward)
        excluded_headers = ['content-encoding', 'content-length',
                            'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response
    return Response(status=500)
    """
    #print(request)
    resp = requests.request(
        method=request.method,
        url=request.url.replace(SITE_NAME, "%s:%s" % (service_address, service_port)),
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    #        files=request.files,



    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    return response
    """



## https://stackoverflow.com/questions/32237379/python-flask-redirect-to-https-from-http
@app.before_request
def before_request():
    pass
    """
    if not request.is_secure and app.env != "development":
        url = request.url.replace("http://", "https://", 1)
        code = 301
        return redirect(url, code=code)
    """

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Flask proxy to forward the requests done to a given port to an other machine")


    class PortAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            if not 0 < values < 2 ** 16:
                raise argparse.ArgumentError(self,
                                             "port numbers must be between 0 and 2**16")
            setattr(namespace, self.dest, values)

    parser.add_argument('-ip', '--input_port',
                        help='Port number to listen to',
                        dest='input_port',
                        default=5000,
                        type=int,
                        choices=range(0, 65536),
                        metavar="{0..65535}")

    parser.add_argument('-sp', '--service_port',
                        help='Port number where the service will be listening',
                        dest='service_port',
                        default=5000,
                        type=int,
                        choices=range(0, 65536),
                        metavar="{0..65535}")

    parser.add_argument('-sa', '--service_address',
                        help='Address where the service will be listening',
                        dest='service_address',
                        default="10.32.3.2",
                        type=str)

    args = parser.parse_args()

    input_port = args.input_port
    service_port = args.service_port
    service_address = args.service_address

    SITE_NAME = "http://%s:%s/" % (service_address, service_port)

    app.env = "development"
    app.run(debug = False,host="0.0.0.0",port=input_port)

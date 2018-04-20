import contextlib
import BaseHTTPServer
import threading
import urlparse
import webbrowser
import requests
import argparse


@contextlib.contextmanager
def serve_once(server_address, request_handler):
    httpd = BaseHTTPServer.HTTPServer(server_address, request_handler)

    thread = threading.Thread(target=httpd.handle_request)
    thread.start()

    yield httpd

    thread.join()
    httpd.server_close()


def main(args):
    request_args = {}

    class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

        def do_GET(self):
            request_args.update(self.get_request_args())

        def get_request_args(self):
            query_params = urlparse.urlparse(self.path).query
            return dict(kv.split("=") for kv in query_params.split("&"))

    redirect_uri = "http://{args.host}:{args.port}".format(args=args)

    with serve_once((args.host, args.port), RequestHandler):
        webbrowser.open(make_get_code_url(
            client_id=args.client_id,
            redirect_uri=redirect_uri,
            scope=args.scope
        ))

    access_token = requests.get(make_get_token_url(
        client_id=args.client_id,
        client_secret=args.client_secret,
        redirect_uri=redirect_uri,
        code=request_args["code"]
    )).json()["access_token"]

    with open("access_token.txt", "w") as f:
        f.write(access_token)


def make_get_code_url(client_id, redirect_uri, scope=""):
    return (
        "https://oauth.vk.com/authorize?"
        "client_id={client_id}&"
        "redirect_uri={redirect_uri}&"
        "scope={scope}&"
        "response_type=code&"
        "display=page"
        .format(**locals())
    )


def make_get_token_url(client_id, client_secret, redirect_uri, code):
    return (
        "https://oauth.vk.com/access_token?"
        "client_id={client_id}&"
        "client_secret={client_secret}&"
        "redirect_uri={redirect_uri}&"
        "code={code}"
        .format(**locals())
    )


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("--host", default="localhost")
    arg_parser.add_argument("--port", type=int, default=8080)
    arg_parser.add_argument("--scope", default="")
    arg_parser.add_argument("client_id", type=int)
    arg_parser.add_argument("client_secret")

    main(arg_parser.parse_args())

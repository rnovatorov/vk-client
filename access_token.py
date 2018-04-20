import argparse
import BaseHTTPServer
import contextlib
import requests
import threading
import urlparse
import webbrowser


def main(args):
    redirect_uri = "http://{args.host}:{args.port}".format(args=args)

    class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

        def do_GET(self):
            request_args = self.get_request_args()

            token_url = make_token_url(
                client_id=args.client_id,
                client_secret=args.client_secret,
                redirect_uri=redirect_uri,
                code=request_args["code"]
            )
            response = requests.get(token_url)
            payload = response.json()
            access_token = payload["access_token"]

            with open(args.out, "w") as f:
                f.write(access_token)

            self.send_response(200)
            self.end_headers()
            self.wfile.write("Success.")

        def get_request_args(self):
            query_params = urlparse.urlparse(self.path).query
            return dict(kv.split("=") for kv in query_params.split("&"))

    server_address = (args.host, args.port)
    with serve_once(server_address, RequestHandler):
        code_url = make_code_url(
            client_id=args.client_id,
            redirect_uri=redirect_uri,
            scope=args.scope
        )
        webbrowser.open(code_url)


@contextlib.contextmanager
def serve_once(server_address, request_handler):
    httpd = BaseHTTPServer.HTTPServer(server_address, request_handler)

    thread = threading.Thread(target=httpd.handle_request)
    thread.start()

    yield

    thread.join()
    httpd.server_close()


def make_code_url(client_id, redirect_uri, scope=""):
    return (
        "https://oauth.vk.com/authorize?"
        "client_id={client_id}&"
        "redirect_uri={redirect_uri}&"
        "scope={scope}&"
        "response_type=code&"
        "display=page"
        .format(**locals())
    )


def make_token_url(client_id, client_secret, redirect_uri, code):
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
    arg_parser.add_argument("--out", default="access-token.txt")
    arg_parser.add_argument("client_id", type=int)
    arg_parser.add_argument("client_secret")

    main(arg_parser.parse_args())

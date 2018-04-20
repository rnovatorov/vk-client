import argparse
import BaseHTTPServer
import contextlib
import requests
import threading
import urlparse
import webbrowser


def auth_code_flow(args):
    redirect_uri = "http://{args.host}:{args.port}".format(args=args)

    class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

        def do_GET(self):
            request_args = self.get_request_args()

            access_token_url = make_access_token_url(
                client_id=args.client_id,
                client_secret=args.client_secret,
                redirect_uri=redirect_uri,
                code=request_args["code"]
            )
            response = requests.get(access_token_url)
            payload = response.json()

            if "access_token" in payload:
                with open(args.out, "w") as f:
                    f.write(payload["access_token"])

            self.end_headers()
            self.wfile.write(response.content)

        def get_request_args(self):
            query_params = urlparse.urlparse(self.path).query
            return dict(kv.split("=") for kv in query_params.split("&"))

    server_address = (args.host, args.port)
    with serve_once(server_address, RequestHandler):
        authorize_url = make_authorize_url(
            client_id=args.client_id,
            redirect_uri=redirect_uri,
            response_type="code",
            scope=args.scope
        )
        webbrowser.open(authorize_url)


def implicit_flow(args):
    authorize_url = make_authorize_url(
        client_id=args.client_id,
        redirect_uri="blank.html",
        response_type="token",
        scope=args.scope
    )
    webbrowser.open(authorize_url)


@contextlib.contextmanager
def serve_once(server_address, request_handler):
    httpd = BaseHTTPServer.HTTPServer(server_address, request_handler)

    thread = threading.Thread(target=httpd.handle_request)
    thread.start()

    yield

    thread.join()
    httpd.server_close()


def make_authorize_url(client_id, redirect_uri, response_type, scope=""):
    return (
        "https://oauth.vk.com/authorize?"
        "client_id={client_id}&"
        "redirect_uri={redirect_uri}&"
        "scope={scope}&"
        "response_type={response_type}&"
        "display=page"
        .format(**locals())
    )


def make_access_token_url(client_id, client_secret, redirect_uri, code):
    return (
        "https://oauth.vk.com/access_token?"
        "client_id={client_id}&"
        "client_secret={client_secret}&"
        "redirect_uri={redirect_uri}&"
        "code={code}"
        .format(**locals())
    )


def create_parser():
    arg_parser = argparse.ArgumentParser()
    subparsers = arg_parser.add_subparsers()

    implicit_parser = subparsers.add_parser("implicit")
    implicit_parser.add_argument("--scope", default="")
    implicit_parser.add_argument("client_id", type=int)
    implicit_parser.set_defaults(handler=implicit_flow)

    authcode_parser = subparsers.add_parser("authcode")
    authcode_parser.add_argument("--host", default="localhost")
    authcode_parser.add_argument("--port", type=int, default=8080)
    authcode_parser.add_argument("--out", default="access-token.txt")
    authcode_parser.add_argument("--scope", default="")
    authcode_parser.add_argument("client_id", type=int)
    authcode_parser.add_argument("client_secret")
    authcode_parser.set_defaults(handler=auth_code_flow)

    return arg_parser


def main():
    arg_parser = create_parser()
    args = arg_parser.parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()

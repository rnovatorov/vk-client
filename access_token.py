import webbrowser
import argparse


def main(args):
    success = get_access_token(
        args.client_id,
        args.scope
    )
    print(success)


def get_access_token(client_id, scope):
    return webbrowser.open(
        "https://oauth.vk.com/authorize?client_id={client_id}&"
        "redirect_uri=https://oauth.vk.com/blank.hmtl&"
        "scope={scope}&"
        "response_type=token&"
        "display=page".format(**locals()))


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("client_id", type=int)
    arg_parser.add_argument(
        "-s",
        dest="scope",
        help="permissions bit mask",
        required=False,
        default=""
    )
    ns = arg_parser.parse_args()
    main(ns)

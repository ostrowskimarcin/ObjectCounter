import argparse


def get_arguments_from_parser() -> argparse.Namespace:
    parser = create_argument_parser()
    args = parser.parse_args()
    return args


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source",
                        help="Specify the path to video source or camera number.")
    parser.add_argument('-d', '--debug',
                        nargs='?',
                        const=True,
                        help="Activate debug mode")
    parser.add_argument('-n', '--notifications',
                        nargs='?',
                        const=True,
                        help="Activate sms notifications")
    parser.add_argument('-p', '--photos',
                        nargs='?',
                        const=True,
                        help="Send photos do google drive"
                        )
    parser.add_argument("-l", "--limit",
                        help="Set the room population limit")
    return parser

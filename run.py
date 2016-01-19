import argparse

from parser import RCGPParser, BSGParser


HTML_PARSER = {
    'rcgp': {
        'klass': RCGPParser,
    },
    'bsg': {
        'klass': BSGParser,
        'url': ''
    }
}


def parse_args():
    args = argparse.ArgumentParser(description="Scrap HTML content")
    args.add_argument('--type', choices=HTML_PARSER.keys(), required=True, type=str,
                        help="Type of Parser (rcgp, bsg)")

    return args.parse_args()


def run():
    args = parse_args()
    try:
        Parser = HTML_PARSER[args.type]['klass']
    except KeyError:
        print "Invalid Type of Parser"
    else:
        tracker = Parser()
        response = tracker.tracker()
        tracker.report(response)


if __name__ == '__main__':
    run()
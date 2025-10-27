import argparse
from dhara.config import DIRS

def main():
    parser = argparse.ArgumentParser(description='Dhara.AI Core CLI')
    sub = parser.add_subparsers(dest='command')
    sub.add_parser('init', help='Initialize Dhara data lake structure')
    args = parser.parse_args()
    if args.command == 'init':
        print('✅ Dhara Data Lake initialized at:', DIRS['raw'].parent)
    else:
        parser.print_help()

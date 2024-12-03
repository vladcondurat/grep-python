import os
import re
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Search for a pattern in files or folders.")
    parser.add_argument("pattern", help="The regex pattern to search for.")
    parser.add_argument("path", help="The file or folder to search in.")
    parser.add_argument("-i", "--ignore-case", action="store_true", help="Ignore case distinctions in the pattern.")
    parser.add_argument("-n", "--not-match", action="store_true", help="Print files without matches instead.")
    parser.add_argument("-c", "--count", action="store_true", help="Print the number of matches instead of matching lines.")
    
    args = parser.parse_args()

    flags = re.IGNORECASE if args.ignore_case else 0
    try:
        regex = re.compile(args.pattern, flags)
    except re.error as e:
        print(f"Invalid regular expression: {e}")
        sys.exit(1)

    if os.path.isfile(args.path):
        process_file(args.path, regex, args)
    elif os.path.isdir(args.path):
        for root, _, files in os.walk(args.path):
            for file in files:
                file_path = os.path.join(root, file)
                process_file(file_path, regex, args)
    else:
        print(f"Path does not exist: {args.path}")
        sys.exit(1)


def process_file(file_path, regex, args):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            contents = f.read()
    except Exception as e:
        print(f"Cannot read file {file_path}: {e}")
        return

    matches = regex.findall(contents)
    num_matches = len(matches)

    if args.not_match:
        handle_not_match(file_path, num_matches, args)
    else:
        handle_match(file_path, regex, num_matches, args)


def handle_not_match(file_path, num_matches, args):
    if num_matches == 0:
        if args.count:
            print(f"{file_path}: 0")
        else:
            print(file_path)


def handle_match(file_path, regex, num_matches, args):
    if args.count:
        print(f"{file_path}: {num_matches}")
    else:
        if num_matches > 0:
            print_matching_lines(file_path, regex)


def print_matching_lines(file_path, regex):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, start=1):
                if regex.search(line):
                    print(f"{file_path}:{line_num}:{line.strip()}")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")


if __name__ == "__main__":
    main()

import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Redis server")
    parser.add_argument(
        "--dir", type=str, help="The directory where RDB files are stored"
    )
    parser.add_argument("--dbfilename", type=str, help="The name of the RDB file")
    return parser.parse_args()

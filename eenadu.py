import os
import logging
import argparse
from utils import Editions, download_and_merge
from parser import eenaduParser
from telegram_post import TelegramPoster

# set logging
if os.getenv("EENADU_DEBUG") is not None:
    logging.basicConfig(level=os.getenv("EENADU_DEBUG"), format='%(levelname)s:%(name)s.py:%(funcName)s:%(message)s')

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="Eenadu(ఈనాడు) ePaper Downloader")
parser.add_argument('-e', '--edition',  type=str, default = "HYDERABAD", 
                    choices = ["ANDHRAPRADESH", "TELANGANA", "HYDERABAD", "SUNDAY"])          
parser.add_argument('-d', '--date', required=False,  type=str, help="date of e-paper (DD/MM/YYYY)")
parser.add_argument('-t', '--telegram', action="store_true", required=False, help="Telegram JSON Config")
parser.add_argument('-c', '--cookies', required=False,  type=str, default="cookies.txt", help="Cookie Dump.")
args = parser.parse_args()

def main():
    logger.debug(args)
    parser = eenaduParser(args.cookies, args.date)
    parser.get_edition(Editions[args.edition.upper()])
    download_and_merge(parser.gen_filename(), parser.get_links())

    if args.telegram:
        t = TelegramPoster("telegram.json")
        t.post(parser.gen_filename())


if __name__ == "__main__":
    main()
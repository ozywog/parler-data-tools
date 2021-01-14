#!/usr/bin/env python3
#Written by Ozywog for Parler Analysis Team

import sys
import internetarchive as ia
from hurry.filesize import size
import concurrent.futures
import logging
import time


def init_download(coll_name, dl_maxsize, dl_threadlimit):
    logformat = "%(asctime)s: %(message)s"
    logging.basicConfig(format=logformat, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info("Main    : Archive download initiated")
    start_time = time.time()
    coll_items = index_collection(dl_maxsize, coll_name)
    download_all_files(coll_items, dl_threadlimit)
    duration = time.time() - start_time
    print(f"Downloaded {len(coll_items)} in {duration} seconds")


def index_collection(dl_maxsize, coll_name):
    num = 0
    coll_itemlist = ia.search_items('collection:'+coll_name)
    itemlist = []
    dl_currentsize = 0
    for result in coll_itemlist:
        num = num + 1  # item count
        itemid = result['identifier']
        logging.info("Main    : Added result #" + str(num) + ": " + str(itemid))

        item = ia.get_item(itemid)
        item_size = item.item_size
        print('Current item size:' + str(size(item_size)))

        if (dl_currentsize + item_size) < dl_maxsize:
            dl_currentsize += item_size
            itemlist.append(item)
        else:
            break

    print("Completed collection indexing to size limit.")
    return itemlist


def downloader(item):
    print('Started thread for item')
    item.download()


def download_all_files(items, threadlimit):

    with concurrent.futures.ThreadPoolExecutor(max_workers=threadlimit) as executor:
        executor.map(downloader, items)



def main():

    collection_name = sys.argv[1]
    dl_limit = int(sys.argv[2])*(2^30)
    thread_limit = int(sys.argv[3])


    init_download(collection_name, dl_limit, thread_limit)

if __name__ == '__main__':
    sys.exit(main())

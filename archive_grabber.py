import internetarchive as ia
from hurry.filesize import size
import concurrent.futures
import logging
import threading
import time

# download size in Bytes, CHANGE THIS
dl_maxsize_final = 5368709120

# downloader thread limit, CHANGE THIS
dl_threadlimit = 20

# change the collection name
collection_name = "officialukplaystationmagazine"  #example

# don't change this
dl_currentsize_final = 0

def init_download():
    logformat = "%(asctime)s: %(message)s"
    logging.basicConfig(format=logformat, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info("Main    : Archive download initiated")
    start_time = time.time()
    coll_items = index_collection(dl_currentsize_final, dl_maxsize_final)
    download_all_files(coll_items, dl_threadlimit)
    duration = time.time() - start_time
    print(f"Downloaded {len(coll_items)} in {duration} seconds")


def index_collection(dl_currentsize, dl_maxsize):
    num = 0
    coll_itemlist = ia.search_items('collection:'+collection_name)
    itemlist = []

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


init_download()

import internetarchive as ia
from hurry.filesize import size
import logging
import threading
import time

# download size in Bytes, CHANGE THIS
dl_maxsize_final = 5368709120

# downloader thread limit, CHANGE THIS
dl_threadlimit = 5

# don't change this
dl_currentsize_final = 0


def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)


def init_download():
    logformat = "%(asctime)s: %(message)s"
    logging.basicConfig(format=logformat, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info("Main    : Archive download initiated")
    download_collection(dl_currentsize_final, dl_maxsize_final, dl_threadlimit)


def download_collection(dl_currentsize, dl_maxsize, threadlimit):

    num = 0
    threadcount = 0

    while dl_currentsize < dl_maxsize:
        threads = []
        while threadcount < threadlimit:
            for result in ia.search_items('collection:archiveteam_neparlepas'):
                num = num + 1  # item count
                itemid = result['identifier']
                logging.info("Main    : initiate dl thread for result #" + str(num) + ": " + str(itemid))

                item = ia.get_item(itemid)
                item_size = item.item_size
                print('Local archive size:' + str(size(dl_currentsize)) + '/' +str(size(dl_maxsize)))
                print('Current item size:' + str(size(item_size)))

                dl_currentsize += item_size
                x = threading.Thread(target=threaded_downloader(item), args=(str(itemid)))
                logging.info("Main    : Executing download thread")
                x.start()
                threads.append(x)
                threadcount += 1

        logging.info("Main    : Thread limit reached, waiting for completion.")
        for t in threads:
            t.join()
        logging.info("Main    : All current threads complete. Continuing.")
        threadcount = 0

    print('Download Limit reached, quitting.')


def threaded_downloader(item):
    item.download()

init_download()

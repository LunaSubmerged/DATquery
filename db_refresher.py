import threading
import time
import schedule
from databases import all_dbs
from databases import attachMoves


def dbRefresh():
    for db in all_dbs:
        db.refresh_db()
    attachMoves()


def dbRefreshScheduler():
    schedule.every().day.at("00:00:00").do(dbRefresh)
    while True:
        schedule.run_pending()
        time.sleep(60)


def start_db_refresher():
    dbRefreshThreads = threading.Thread(target = dbRefreshScheduler)
    dbRefreshThreads.start()

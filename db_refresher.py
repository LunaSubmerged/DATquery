
def dbRefresh():
    for db in databases:
        db.refresh_db()
    attachMoves()
def dbRefreshScheduler():
    schedule.every().day.at("00:00:00").do(dbRefresh)
    while True:
        schedule.run_pending()
        time.sleep(60)
        

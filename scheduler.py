from apscheduler.schedulers.blocking import BlockingScheduler
from batch_predict import run_batch_prediction

scheduler = BlockingScheduler()
scheduler.add_job(run_batch_prediction, "interval", minutes=5)

if __name__ == "__main__":
    print("Starting batch scheduler (every 5 minutes)...")
    run_batch_prediction()  # Run once immediately
    scheduler.start()
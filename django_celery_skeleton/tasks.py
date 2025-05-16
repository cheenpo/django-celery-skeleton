from celery import shared_task
import time
    
@shared_task
def my_task(self, num):
    try:
        time.sleep(10)  # Simulate a long-running task
        return f"Task completed with result: {num * 2}"
    except Exception as e:
        raise self.retry(exc=e, countdown=5, max_retries=3)

from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import httpx
import logging

# Initialize the FastAPI app
app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to perform the ping
async def ping_url():
    url = "https://rideshare-h8sq.onrender.com/rides"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            logger.info(f"Ping successful: {response.status_code}")
        except httpx.HTTPStatusError as e:
            logger.error(f"Ping failed: {e}")

# Setup the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(
    ping_url,
    IntervalTrigger(minutes=10),  # Trigger every 10 minutes
    id='ping_job',
    name='Ping the rides URL every 10 minutes',
    replace_existing=True
)
scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

@app.get("/")
def read_root():
    return {"message": "Ping service is running"}


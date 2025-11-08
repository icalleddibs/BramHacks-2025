"""
Data fetcher
Currently using NASA earthaccess

"""
import earthaccess
import xarray as xr
from datetime import datetime
#import copernicusmarine
import logging
import os


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_fetch.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create all data directories
os.makedirs("./data/microplastics", exist_ok=True)
os.makedirs("./data/chlorophyll", exist_ok=True)

# Authenticate with NASA Earthdata
logger.info("Authenticating with NASA Earthdata...")
earthaccess.login()

# Define date range
start_date = "2024-01-01"
end_date = "2024-12-31"

# Define bounding box - [min_lon, min_lat, max_lon, max_lat]
#bbox = [-128, -60, 68, 58]
bbox = [-180, -90, 180, 90]  # Whole Earth

logger.info("Searching for datasets...")
logger.info(f"Date range: {start_date} to {end_date}")
logger.info(f"Bounding box: {bbox}")

# 1. MICROPLASTICS
# Using CYGNSS Level 3 number density (#/km^2) daily resolution
logger.info("=" * 50)
logger.info("MICROPLASTICS")
logger.info("=" * 50)
sst_results = earthaccess.search_data(
    short_name='CYGNSS_L3_MICROPLASTIC_V3.2',
    temporal=(start_date, end_date),
)
logger.info(f"Found {len(sst_results)} microplastics granules")

# 2. CURRENTS
# Using OSCAR surface current database 0.25 degree resolution)
logger.info("=" * 50)
logger.info("CURRENTS")
logger.info("=" * 50)
sst_results = earthaccess.search_data(
    short_name='OSCAR_L4_OC_NRT_V2.0',
    temporal=(start_date, end_date),
)
logger.info(f"Found {len(sst_results)} current granules")

logger.info("=" * 50)
logger.info("COMPLETE!")
logger.info("=" * 50)
# # This file contains utility functions for rate limiting API calls.

import hashlib
import json
import logging
import os
import time
from datetime import datetime
from functools import wraps

# Create a temporary directory for usage data files
TEMP_DIR = ".api_usage_data"
os.makedirs(TEMP_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class RateLimitException(Exception):
    pass


def get_usage_file_name(func):
    hash_obj = hashlib.sha256(func.__name__.encode())
    return os.path.join(TEMP_DIR, f"{hash_obj.hexdigest()}.json")


# #original
# def check_rate_limit(usage_data, limit, period, wait):
#     current_time = int(time.time())
#     period_name = {1: "second", 60: "minute", 60 * 60: "hour", 24 * 60 * 60: "day", 30 * 24 * 60 * 60: "month"}[period]
#     period_start = usage_data.get(f"last_reset_{period_name}", current_time)
#     period_end = period_start + period
#     if current_time < period_end:
#         requests_this_period = usage_data.get(f"requests_this_{period_name}", 0)
#         if requests_this_period >= limit:
#             logging.warning(f"Rate limit reached: {requests_this_period}/{limit} requests per {period_name}.")
#             if wait:
#                 # Calculate the wait time until the next period
#                 wait_time = period_end - current_time
#                 logging.info(f"Waiting {wait_time} seconds due to rate limit for {period_name}.")
#                 time.sleep(wait_time)
#                 # Reset the usage data for the next period
#                 usage_data[f"last_reset_{period_name}"] = current_time + period
#                 usage_data[f"requests_this_{period_name}"] = 1
#             else:
#                 logging.error(f"Rate limit reached for requests per {period_name}.")
#                 return True
#         else:
#             usage_data[f"requests_this_{period_name}"] = requests_this_period + 1
#     else:
#         # If the current time has exceeded the period, reset the usage data
#         usage_data[f"last_reset_{period_name}"] = current_time
#         usage_data[f"requests_this_{period_name}"] = 1
#     return False


def check_rate_limit(usage_data, limit, period, wait):
    current_time = int(time.time())
    period_name = {
        1: "second",
        60: "minute",
        60 * 60: "hour",
        24 * 60 * 60: "day",
        30 * 24 * 60 * 60: "month",
    }[period]
    period_start = usage_data.get(f"last_reset_{period_name}", current_time)
    period_end = period_start + period

    # Handle case where current time is within the same period
    if current_time < period_end:
        requests_this_period = usage_data.get(f"requests_this_{period_name}", 0)
        if requests_this_period >= limit:
            logging.warning(
                f"Rate limit reached: {requests_this_period}/{limit} requests per {period_name}."
            )
            if wait:
                wait_time = period_end - current_time
                logging.info(
                    f"Waiting {wait_time} seconds due to rate limit for {period_name}."
                )
                time.sleep(wait_time)
                usage_data[f"last_reset_{period_name}"] = current_time + period
                usage_data[f"requests_this_{period_name}"] = 1
            else:
                logging.error(f"Rate limit reached for requests per {period_name}.")
                return True
        else:
            usage_data[f"requests_this_{period_name}"] = requests_this_period + 1
    else:
        usage_data[f"last_reset_{period_name}"] = current_time
        usage_data[f"requests_this_{period_name}"] = 1

    # Keep track of request timestamps within the same second
    usage_data.setdefault("request_times", []).append(current_time)
    usage_data["request_times"] = [
        t for t in usage_data["request_times"] if current_time - t < 1
    ]
    requests_this_second = len(usage_data["request_times"])

    # Check if requests made within the same second exceed the limit
    if requests_this_second > limit:
        logging.warning(
            f"Rate limit reached: {requests_this_second}/{limit} requests per second."
        )
        if wait:
            wait_time = 1 - (current_time - usage_data["request_times"][0])
            logging.info(f"Waiting {wait_time} seconds due to rate limit for second.")
            time.sleep(wait_time)
        else:
            logging.error("Rate limit reached for requests per second.")
            return True

    return False


def rate_limiter(
    requests_per_second=None,
    requests_per_minute=None,
    requests_per_hour=None,
    requests_per_day=None,
    requests_per_month=None,
    wait=False,
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            USAGE_FILE = get_usage_file_name(func)
            try:
                with open(USAGE_FILE, "r") as f:
                    usage_data = json.load(f)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                usage_data = {}

            # Check the more restrictive limit first
            if requests_per_second:
                if check_rate_limit(usage_data, requests_per_second, 1, wait):
                    return
            if requests_per_minute:
                if check_rate_limit(usage_data, requests_per_minute, 60, wait):
                    return
            if requests_per_hour:
                if check_rate_limit(usage_data, requests_per_hour, 60 * 60, wait):
                    return
            if requests_per_day:
                if check_rate_limit(usage_data, requests_per_day, 24 * 60 * 60, wait):
                    return
            if requests_per_month:
                if check_rate_limit(
                    usage_data, requests_per_month, 30 * 24 * 60 * 60, wait
                ):
                    return

            with open(USAGE_FILE, "w") as f:
                json.dump(usage_data, f)

            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator

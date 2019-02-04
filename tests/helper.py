import logging
import time

def run_until_true(test, tries=5, backoff=2, delay=30):
    current_try = 0
    logging.getLogger().info('Initiating retry loop: tries=%d, backoff=%d, delay=%d', tries, backoff, delay)
    while(current_try < tries):
        if test() is True:
            return True
        logging.getLogger().info('Attempt %d', current_try)
        time.sleep(delay * (backoff ** current_try))
        current_try += 1
    logging.getLogger().error('Check has timed out.')
    return False
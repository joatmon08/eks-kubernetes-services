import logging
import time

TEST_FIXTURE_HEADERS = {
    'Host': 'ingress-e2e.joatmon08.com'
}

def ingress_is_created(k8s_extensions, test_application_name, namespace):
    return k8s_extensions.read_namespaced_ingress_status(test_application_name, namespace).status.load_balancer.ingress


def service_is_created(k8s_core, namespace, label):
    return k8s_core.list_namespaced_service(namespace, label_selector=label).items[0].status.load_balancer.ingress[0].hostname


def run_until_not_none(test, tries=5, backoff=2, delay=30):
    current_try = 0
    logging.getLogger().info(
        'Initiating retry loop: tries=%d, backoff=%d, delay=%d', tries, backoff, delay)
    while(current_try < tries):
        if test() is not None:
            return True
        logging.getLogger().info('Attempt %d', current_try)
        time.sleep(delay * (backoff ** current_try))
        current_try += 1
    logging.getLogger().error('Check has timed out.')
    return False

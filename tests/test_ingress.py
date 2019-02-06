import pytest
import logging
import helper
import requests

def test_should_have_ingress(caplog, kubernetes_client, release, namespace):
    caplog.set_level(logging.INFO)
    logging.getLogger().info('Checking if Ingress has been created')

    test_application_name = "{0}-ingress-e2e".format(release)

    def ingress_is_created(): return kubernetes_client.read_namespaced_ingress_status(
        test_application_name, namespace).status.load_balancer.ingress

    assert helper.run_until_not_none(ingress_is_created) is True


def test_should_connect_to_ingress_hostname(caplog, kubernetes_client, release, namespace):
    caplog.set_level(logging.INFO)
    logging.getLogger().info('Checking if we can connect to ingress hostname')

    test_application_name = "{0}-ingress-e2e".format(release)

    def ingress_is_created(): return kubernetes_client.read_namespaced_ingress_status(
        test_application_name, namespace).status.load_balancer.ingress

    helper.run_until_not_none(ingress_is_created)

    hostname = kubernetes_client.read_namespaced_ingress_status(
        test_application_name, namespace).status.load_balancer.ingress[0].hostname

    headers = {
        'Host': 'ingress-e2e.joatmon08.com'
    }

    def check_endpoint_is_ready():
        try:
            response = requests.get("http://{0}/health".format(hostname), headers=headers)
            response.raise_for_status()
            return response
        except:
            return None

    helper.run_until_not_none(check_endpoint_is_ready)

    response = check_endpoint_is_ready()
    assert response.status_code == 200
    assert response.content == b'This is a pretend health endpoint.'

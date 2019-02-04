import pytest
import logging
import helper
import requests


def test_should_have_ingress(caplog, kubernetes_client, release, namespace):
    caplog.set_level(logging.INFO)
    logging.getLogger().info('Checking if Ingress has been created')

    test_application_name = "{0}-ingress-e2e".format(release)

    def ingress_is_created(): return (kubernetes_client.read_namespaced_ingress_status(
        test_application_name, namespace).status.load_balancer.ingress is not None)

    assert helper.run_until_true(ingress_is_created) is True


def test_should_connect_to_ingress_hostname(caplog, kubernetes_client, release, namespace):
    caplog.set_level(logging.INFO)
    logging.getLogger().info('Checking if we can connect to ingress hostname')

    test_application_name = "{0}-ingress-e2e".format(release)

    def ingress_is_created(): return (kubernetes_client.read_namespaced_ingress_status(
        test_application_name, namespace).status.load_balancer.ingress is not None)

    helper.run_until_true(ingress_is_created)

    hostname = kubernetes_client.read_namespaced_ingress_status(
        test_application_name, namespace).status.load_balancer.ingress[0].hostname

    headers = {
        'Host': 'ingress-e2e.joatmon08.com'
    }
    response = requests.get("http://{0}/hello".format(hostname), headers=headers)
    response.raise_for_status()

    assert response.status_code == 200
    assert response.content == 'Hello World!'

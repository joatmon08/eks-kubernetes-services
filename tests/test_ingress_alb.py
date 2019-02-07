import pytest
import logging
import helper
import requests

@pytest.mark.alb
def test_should_have_ingress_alb(caplog, k8s_extensions, test_application_name, namespace):
    caplog.set_level(logging.INFO)
    logging.getLogger().info('Checking if Ingress has been created')

    assert helper.run_until_not_none(lambda: helper.ingress_is_created(
        k8s_extensions, test_application_name, namespace))


@pytest.mark.alb
def test_should_connect_to_ingress_alb_hostname(caplog, k8s_extensions, test_application_name, namespace):
    caplog.set_level(logging.INFO)
    logging.getLogger().info('Checking if we can connect to ingress hostname')

    helper.run_until_not_none(lambda: helper.ingress_is_created(
        k8s_extensions, test_application_name, namespace))

    hostname = helper.ingress_is_created(
        k8s_extensions, test_application_name, namespace)[0].hostname

    def check_endpoint_is_ready():
        try:
            response = requests.get(
                "http://{0}/health".format(hostname), headers=helper.TEST_FIXTURE_HEADERS)
            response.raise_for_status()
            return response
        except:
            return None

    helper.run_until_not_none(check_endpoint_is_ready)

    response = check_endpoint_is_ready()
    assert response.status_code == 200
    assert response.content == b'This is a pretend health endpoint.'

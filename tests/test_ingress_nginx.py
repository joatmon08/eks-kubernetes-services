import pytest
import logging
import helper
import requests

NGINX_CONTROLLER_NAMESPACE = 'kube-system'
NGINX_LABEL = 'app=nginx-ingress'


@pytest.mark.nginx
def test_should_have_ingress_nginx(caplog, k8s_extensions, test_application_name, namespace):
    caplog.set_level(logging.INFO)
    logging.getLogger().info('Checking if Ingress has been created')

    assert helper.run_until_not_none(lambda: helper.ingress_is_created(
        k8s_extensions, test_application_name, namespace))


@pytest.mark.nginx
def test_should_connect_to_ingress_nginx_hostname(caplog, k8s_core):
    caplog.set_level(logging.INFO)
    logging.getLogger().info('Checking if we can connect to ingress hostname')

    helper.run_until_not_none(lambda: helper.service_is_created(
        k8s_core, NGINX_CONTROLLER_NAMESPACE, NGINX_LABEL))

    hostname = helper.service_is_created(
        k8s_core, NGINX_CONTROLLER_NAMESPACE, NGINX_LABEL)

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

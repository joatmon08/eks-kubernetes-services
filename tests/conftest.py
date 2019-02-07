#pylint: disable=W0621
import pytest
import kubernetes


def pytest_addoption(parser):
    parser.addoption("--release", action="store", default="e2etests", help="release name")
    parser.addoption("--namespace", action="store", default="default", help="namespace")


@pytest.fixture
def release(request):
    return request.config.getoption("--release")


@pytest.fixture
def test_application_name(request):
    return "{0}-ingress-e2e".format(request.config.getoption("--release"))


@pytest.fixture
def namespace(request):
    return request.config.getoption("--namespace")


@pytest.fixture
def k8s_extensions():
    kubernetes.config.load_kube_config()
    return kubernetes.client.ExtensionsV1beta1Api()


@pytest.fixture
def k8s_core():
    kubernetes.config.load_kube_config()
    return kubernetes.client.CoreV1Api()


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
def namespace(request):
    return request.config.getoption("--namespace")

@pytest.fixture
def kubernetes_client():
    kubernetes.config.load_kube_config()
    return kubernetes.client.ExtensionsV1beta1Api()



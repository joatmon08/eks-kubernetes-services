# eks-kubernetes-services

These are examples of services that can deployed to EKS.

## Pre-Requisites
1. Helm v2.12.3
1. AWS EKS (Kubernetes v1.11.5)
1. Python3 & pip

## Setting Up
Most of these are based on Helm charts.

1. Set up your cluster on AWS EKS. Make sure you know the name of it.
1. Install Python invoke task framework using `pip install -r requirements.txt`.
1. Run `invoke helm.setup` in order to deploy tiller with RBAC.
1. Run `invoke helm.install-charts` to install the dependencies for the charts.
1. Copy `values.yaml` and rename it to `values.[cluster name].yaml`.
1. Update `values.[cluster name].yaml` with the correct values for AWS
   account & cluster.

## Deploy the Services
1. To edit the services you wish to deploy, you'll need to update the `charts/`
directory, `requirements.yaml`, and `values.[cluster name].yaml`.
1. Then, install the services via:
   ```
   invoke helm.deploy --cluster [cluster name] --release [release] --namespace kube-system
   ```

## Test the Services
All tests for the services are located under the `tests` directory.
```
invoke helm.test --chart [chart name] --name test --namespace e2e
```
This will deploy a test application via Helm and run a test using pytest.

## Cleanup
```
invoke helm.clean --release [release]
```
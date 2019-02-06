setup:
	kubectl apply -f tiller/
	helm init --service-account tiller
	helm version

dependencies:
	helm repo add kube2iam http://storage.googleapis.com/kubernetes-charts
	helm repo add aws-alb-ingress-controller http://storage.googleapis.com/kubernetes-charts-incubator
	helm dependency update

test:
	helm install tests/ingress-e2e --name tests --namespace e2e
	pytest tests --release tests --namespace e2e
	helm del --purge tests

deploy:
	AWS_EKS_CLUSTER_NAME=$(shell 'kubectl config current-context | awk -F "@|.us" "{print $2}"')
	#helm install -f values.$(AWS_EKS_CLUSTER_NAME).yaml . --name services --namespace kube-system

clean:
	helm del --purge services
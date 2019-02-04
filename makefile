setup:
	kubectl apply -f tiller/
	helm init --service-account tiller
	helm version

dependencies:
	helm repo add kube2iam http://storage.googleapis.com/kubernetes-charts
	helm repo add aws-alb-ingress-controller http://storage.googleapis.com/kubernetes-charts-incubator
	helm dependency update

test:
	helm install tests/ingress-e2e --name e2etests
	pytest tests --release e2etests
	helm del --purge e2etests

deploy:
	helm install . --name services

clean:
	helm del --purge services
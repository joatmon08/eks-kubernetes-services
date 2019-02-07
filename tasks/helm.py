from invoke import task

@task
def setup(ctx):
    ctx.run('kubectl apply -f tiller/')
    ctx.run('helm init --service-account tiller')
    ctx.run('helm version')


@task
def install_charts(ctx):
    ctx.run('helm repo add kube2iam http://storage.googleapis.com/kubernetes-charts')
    ctx.run(
        'helm repo add nginx-ingress http://storage.googleapis.com/kubernetes-charts')
    ctx.run('helm repo add aws-alb-ingress-controller http://storage.googleapis.com/kubernetes-charts-incubator')
    ctx.run('helm dependency update')


@task
def deploy(ctx, cluster, release, namespace):
    ctx.run(
        'helm install -f values.{0}.yaml . --name {1} --namespace {2}'.format(cluster, release, namespace))


@task
def test(ctx, chart, service, name, namespace):
    ctx.run('helm install  -f tests/{0}/values.{1}.yaml tests/{0} --name {2} --namespace {3}'.format(
        chart, service, name, namespace))
    ctx.run('pytest tests -m {0} --release {1} --namespace {2}'.format(service, name, namespace))
    ctx.run('helm del --purge {0}'.format(name))


@task
def clean(ctx, release):
    ctx.run('helm del --purge {0}'.format(release))

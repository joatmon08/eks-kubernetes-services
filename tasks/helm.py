from invoke import task

@task
def setup(ctx):
    ctx.run('kubectl apply -f tiller/')
    ctx.run('helm init --service-account tiller')
    ctx.run('helm version')


@task
def install_charts(ctx):
    ctx.run('helm repo add kube2iam http://storage.googleapis.com/kubernetes-charts')
    ctx.run('helm repo add aws-alb-ingress-controller http://storage.googleapis.com/kubernetes-charts-incubator')
    ctx.run('helm dependency update')


@task
def deploy(ctx, cluster, release, namespace):
    ctx.run(
        'helm install -f values.{0}.yaml . --name {1} --namespace {2}'.format(cluster, release, namespace))


@task
def test(ctx, chart, name, namespace):
    ctx.run('helm install tests/{0} --name {1} --namespace {2}'.format(chart, name, namespace))
    ctx.run('pytest tests --release {0} --namespace {1}'.format(name, namespace))
    ctx.run('helm del --purge {0}'.format(name))


@task
def clean(ctx, release):
    ctx.run('helm del --purge {0}'.format(release))

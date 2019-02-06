from invoke import Collection
from . import helm

ns = Collection()

ns.add_collection(helm, 'helm')

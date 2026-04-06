from importlib.metadata import distribution as _distribution, PackageNotFoundError

class _Distribution:
    def __init__(self, dist):
        self.version = dist.version

def get_distribution(name):
    return _Distribution(_distribution(name))

DistributionNotFound = PackageNotFoundError

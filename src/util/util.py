import itertools


def generate_possible_configurations(options):
	return list(itertools.product(*list(options.values())))

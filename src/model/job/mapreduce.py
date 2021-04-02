import copy

from src.model.job.feature import Feature


class MapReduce(object):

	def __init__(self, name, config):
		self.name = name
		self.features = []
		self.feature_names = []
		self.execution_time = None
		self.set_configs(config)

	def to_input_array(self):
		return [getattr(self, feature.name) for feature in self.features]

	def clone(self):
		return copy.deepcopy(self)

	def set_configs(self, config: dict):
		for feature_dict in config.get('features', []):
			key = list(feature_dict.keys())[0]
			self.features.append(Feature(key, feature_dict[key].get('required'), feature_dict[key].get('values')))
			self.feature_names.append(key)
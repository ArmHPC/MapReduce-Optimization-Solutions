import json
import os


class ConfigurationProviderService:

	def __init__(self):
		self.configs = {}
		self.configurations_path = 'configurations'

	def get_configuration(self, job_name):
		path = os.path.join(os.path.dirname(__file__),
							self.configurations_path,
							f'{job_name.lower()}.json')
		return self.configs.get(path, self.__read_config(path, job_name))

	def __read_config(self, path, job_name):
		try:
			with open(path, 'rb') as f:
				obj = json.load(f)
				self.configs[path] = obj
				return obj
		except IOError:
			raise IOError(f"Cannot find configuration for application {job_name}")

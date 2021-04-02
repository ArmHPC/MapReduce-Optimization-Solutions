import os
import pickle
from abc import ABC


class BaseProvider(ABC):

	def __init__(self, objects, directory, prefix):
		self.objects = objects
		self.directory = directory
		self.prefix = prefix

	def get_object(self, job_name: str):
		path = os.path.join(self.directory, self.prefix, f'{job_name.lower()}.pkl')
		if path in self.objects:
			return self.objects.get(path)
		else:
			try:
				with open(path, 'rb') as f:
					obj = pickle.load(f)
					self.objects[path] = obj
					return obj
			except IOError:
				raise IOError(f"Invalid application name {job_name}")

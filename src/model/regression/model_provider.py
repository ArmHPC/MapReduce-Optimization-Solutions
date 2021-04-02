import os

from src.model.base_provider import BaseProvider


class RegressionModelProvider(BaseProvider):

	def __init__(self):
		super().__init__(objects={}, directory=os.path.dirname(__file__), prefix='dump')

	def get_model(self, job_name: str):
		return self.get_object(job_name)

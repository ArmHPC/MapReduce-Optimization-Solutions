import json

from src.model.job.mapreduce import MapReduce
from src.service.helper.configuration_provider_service import ConfigurationProviderService


class SerializationService(object):
	configuration_provider_service = ConfigurationProviderService()

	@staticmethod
	def serialize(job: MapReduce):
		return json.dumps(SerializationService.generate_dict(job))

	@staticmethod
	def bulk_serialize(jobs):
		return json.dumps([SerializationService.generate_dict(job) for job in jobs])

	@classmethod
	def deserialize(cls, job_name, request_data, check_required_fields):
		config = cls.configuration_provider_service.get_configuration(job_name)
		job = MapReduce(name=job_name, config=config)
		if not cls.__validate_request_body(job, list(request_data.keys())):
			raise ValueError(f'Invalid request data.')
		cls.set_job_properties(job, request_data, check_required_fields)
		cls.validate_request_data(job)
		return job

	@staticmethod
	def set_job_properties(job: MapReduce, json_data, check_required_fields):
		for feature in job.features:
			value = json_data.get(feature.name)
			if (feature.required or check_required_fields) and value is None:
				raise ValueError(f'{feature.name} value is required')
			setattr(job, feature.name, value)

	@staticmethod
	def generate_dict(job: MapReduce):
		feature_names = job.feature_names + ['execution_time']
		return {feature: job.__getattribute__(feature) for feature in feature_names}

	@staticmethod
	def __validate_request_body(job: MapReduce, body_keys: list):
		return set(job.feature_names).issuperset(set(body_keys))

	@classmethod
	def validate_request_data(cls, job: MapReduce):
		if hasattr(job, 'data_size_gb') and job.__getattribute__('data_size_gb') <= 0:
			raise ValueError(f'Data size must be positive.')
		if hasattr(job, 'nodes_count') and job.__getattribute__('nodes_count') is not None and \
				(not isinstance(job.__getattribute__('nodes_count'), int) or
				 job.__getattribute__('nodes_count') <= 0):
			raise ValueError(f'Nodes count must be positive integer.')
		if hasattr(job, 'cluster_count') and \
				job.__getattribute__('cluster_count') is not None and \
				(not isinstance(job.__getattribute__('cluster_count'), int) or
				 job.__getattribute__('cluster_count') <= 1):
			raise ValueError(f'Clusters count must be positive integer and more than 1.')
		if hasattr(job, 'compression') and \
				job.__getattribute__('compression') != 'none' and \
				job.__getattribute__('ram_over_hdfs'):
			raise ValueError(f'You cannot use compression methods and ram over hdfs together.')

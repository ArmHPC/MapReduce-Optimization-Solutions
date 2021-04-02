import numpy as np

from src.model.job.mapreduce import MapReduce
from src.service.prediction_service import PredictionService
from src.util.util import generate_possible_configurations


class RecommendationService:

	def __init__(self, prediction_service: PredictionService):
		self.prediction_service = prediction_service

	def recommend(self, job: MapReduce, count: int):
		jobs = self.__generate_possible_configs(job)
		predictions = np.array(self.prediction_service.predict(jobs))
		sort_indexes = np.argsort(predictions)
		for i in sort_indexes:
			jobs[i].execution_time = predictions[i]
		return jobs[sort_indexes] if count == 0 else jobs[sort_indexes][:count]

	def __generate_possible_configs(self, job: MapReduce):
		configs, empty_features = self.__get_configs(job)
		jobs = []
		for new_config in configs:
			cloned_job = job.clone()
			for feature_id, empty_feature_name in enumerate(empty_features.keys()):
				cloned_job.__setattr__(empty_feature_name, new_config[feature_id])
			if not (hasattr(cloned_job, 'compression') and
					cloned_job.__getattribute__('compression') != 'none' and
					hasattr(cloned_job, 'ram_over_hdfs') and
					cloned_job.__getattribute__('ram_over_hdfs')):
				jobs.append(cloned_job)
		return np.array([job]) if len(jobs) == 0 else np.array(jobs)

	@staticmethod
	def __get_configs(job: MapReduce):
		empty_features = {}
		for feature in job.features:
			if job.__getattribute__(feature.name) is None:
				empty_features[feature.name] = feature.values
		return generate_possible_configurations(empty_features), empty_features

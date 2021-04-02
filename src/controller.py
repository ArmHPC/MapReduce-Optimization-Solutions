from flask import Flask, jsonify
from flask import request

from src.model.encoder.encoder_provider import EncoderProvider
from src.model.polynomial_features.feature_transformer_provider import FeatureTransformerProvider
from src.model.regression.model_provider import RegressionModelProvider
from src.service.helper.serialization_service import SerializationService
from src.service.prediction_service import PredictionService
from src.service.recommendation_service import RecommendationService

controller = Flask(__name__)
model_provider = RegressionModelProvider()
encoder_provider = EncoderProvider()
feature_transformer_provider = FeatureTransformerProvider()
prediction_service = PredictionService(model_provider, encoder_provider, feature_transformer_provider)
recommendationService = RecommendationService(prediction_service)


@controller.route('/predict/<job_name>', methods=['POST'])
def predict(job_name: str):
	job = SerializationService.deserialize(job_name, request.get_json(), check_required_fields=True)
	job.execution_time = prediction_service.predict([job])[0]
	return SerializationService.serialize(job)


@controller.route('/recommend/<job_name>/<count>', methods=['POST'])
def recommend(job_name: str, count: int):
	try:
		count = int(count)
	except ValueError:
		raise ValueError("Count must be an integer")
	job = SerializationService.deserialize(job_name, request.get_json(), check_required_fields=False)
	jobs = recommendationService.recommend(job, count)
	return SerializationService.bulk_serialize(jobs)


@controller.errorhandler(Exception)
def handle_error(error):
	return jsonify(error=str(error))


if __name__ == '__main__':
	controller.run()

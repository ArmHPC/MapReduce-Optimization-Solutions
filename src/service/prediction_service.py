import numpy as np
import pandas as pd

from src.model.encoder.encoder_provider import EncoderProvider
from src.model.polynomial_features.feature_transformer_provider import FeatureTransformerProvider
from src.model.regression.model_provider import RegressionModelProvider


class PredictionService:

	def __init__(self, model_provider: RegressionModelProvider,
				 encoder_provider: EncoderProvider,
				 feature_transformer_provider: FeatureTransformerProvider):
		self.model_provider = model_provider
		self.encoder_provider = encoder_provider
		self.feature_transformer_provider = feature_transformer_provider

	def predict(self, jobs):
		features = jobs[0].feature_names
		job_name = jobs[0].name
		input_df = pd.DataFrame([job.to_input_array() for job in jobs], columns=features)
		model = self.model_provider.get_model(job_name)
		encoder = self.encoder_provider.get_encoder(job_name)
		feature_transformer = self.feature_transformer_provider \
			.get_feature_transformer(job_name)
		input_data = feature_transformer.transform(encoder.transform(input_df))
		pred = model.predict(input_data)
		return np.round(np.exp(pred))

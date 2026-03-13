# Backend Layer

This folder will contain the FastAPI application.

Role in the app:
- load the trained model artifact
- expose API endpoints like `/health` and `/predict`
- validate request data
- return prediction results as JSON

This layer should not retrain models or read the raw training CSVs.

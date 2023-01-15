# -IUM-Projekt

## Preparing the environment
This project uses [Poetry](https://python-poetry.org) to manage python and its dependencies.

To prepare the environment [install](https://python-poetry.org/docs/#installation) Poetry and run
```
poetry install
poetry shell
```
or install the dependencies listed in `pyproject.toml` manually.

## Running the service
First generate data requred to train predictors:
```
python src/generate_data.py
```
Then start the service:
```
python src/run_service.py
```
This will start the service on port `8888`. Press `ctrl + c` to stop it.

The service has 3 endpoints:
- POST `/avg` - provides a solution using the `DailyCostPredictorAvg` predictor
- POST `/linear` - provides a solution using the  `DailyCostPredictorLinearByDuration` predictor
- POST `/ab` - provides a solution dividing tracks into two groups equally for A/B testing. Pass methods of groups A and B using `a-method` and `b-method` headers.

In the request body provide a JSON compatible with the ServiceInput type defined in [models.py](./src/datamodels/models.py). The only necessary attributes for tracks are `track_id`, `popularity` and (for method `linear`) `duration_ms`.

## Recreating experiments
```
# show info about provided data
python src/analyze_provided_data.py

# generate data required for training predictors
python src/generate_data.py

# analyze generated data
python src/analyze_generated_data.py

# test the accuracy of predictors
python src/analyze_predictors.py

# generate solutions for the provided set of tracks
python src/generate_solutions.py

# show info about generated solutions
python src/analyze_solutions.py
```

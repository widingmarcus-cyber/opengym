# Challenge 114: Partial Failure Recovery

The data pipeline in `setup/pipeline.py` processes records from `setup/data.json`. Currently 7 out of 10 records process successfully, but 3 fail for different reasons.

Fix the pipeline so ALL 10 records process correctly.

**Important:** do not break the 7 records that already work.

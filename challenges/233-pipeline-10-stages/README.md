# Challenge 233: 10-Stage Pipeline

## Objective

Execute a 10-stage data processing pipeline where each stage depends on the output of the previous stage. You must process input data through all 10 stages in the correct order and produce valid output at every stage.

## Setup

- `setup/pipeline.json` defines the 10 pipeline stages in order, including each stage's name, operation, and configuration.
- `setup/input_data.json` contains the raw input records to feed into stage 1.

## Stages

The pipeline has 10 stages that must execute in this exact order:

1. **parse** - Parse raw string records into structured objects
2. **validate** - Validate each record against the schema; mark invalid records
3. **transform** - Apply field transformations (rename, retype, compute derived fields)
4. **enrich** - Enrich records by looking up region from country codes using the provided mapping
5. **dedupe** - Remove duplicate records based on the `id` field, keeping the first occurrence
6. **sort** - Sort records by the configured sort key in ascending order
7. **partition** - Partition records into groups based on the configured partition key
8. **aggregate** - Compute aggregates (count, sum, avg) for each partition
9. **format** - Format the final output into the configured output structure
10. **emit** - Write the final results to the output file

## Task

1. Read `setup/pipeline.json` to understand each stage's configuration.
2. Read `setup/input_data.json` for the raw input data.
3. Execute each stage in order, feeding the output of one stage as input to the next.
4. Write `setup/stage_outputs.json` containing the output of every stage (keyed by stage name).
5. Write `setup/pipeline_result.json` containing the final emitted result.

## Output Format

`setup/stage_outputs.json` must be a JSON object with keys matching each stage name, and values being the output of that stage.

`setup/pipeline_result.json` must contain the final pipeline output as produced by the emit stage.

## Constraints

- Each stage must use ONLY the output of the previous stage as input (stage 1 uses input_data.json).
- Invalid records identified in the validate stage must be excluded from subsequent stages.
- The pipeline must process all 10 stages; partial execution is not acceptable.

# Data versioning

This project uses a lightweight hash-based manifest instead of DVC.

## Why not DVC

DVC (Data Version Control) is the standard tool for this and would be the
right choice for a team project with a remote data store (S3, GCS, etc.).
For a single-file, 210-row dataset with no remote storage in play, adding
a DVC-tracked cache and `.dvc` pointer files is overhead without a matching
benefit — so this project uses the simpler approach below instead, and
notes the migration path if the project grows.

## What's here instead

Every time `src/02_train_and_evaluate.py` runs, it calls
`write_data_version_manifest()` (in `src/utils.py`), which writes
`data/DATA_VERSION.json`:

```json
{
  "file": "clean_data.csv",
  "sha256_12": "e6227e559bec",
  "n_rows": 210,
  "n_sle": 105,
  "n_healthy": 105,
  "columns": ["IFIT3", "IFIH1", "CXCL10", "STAT2", "Label"],
  "generated_at": "2026-01-01T00:00:00+00:00"
}
```

That `sha256_12` hash is also attached to every entry in
`experiments/experiment_log.jsonl` (see below) as `dataset_version`. So for
any experiment record, you can answer "was this run on the same data as
that other run?" by comparing hashes — without opening either CSV.

## Experiment tracking

`src/utils.py` also provides `log_experiment()`, used by
`02_train_and_evaluate.py`, `05_nested_cv.py`, and `06_ablation_study.py`.
Each call appends one JSON line to a file under `experiments/` with:

- `experiment_id`, `timestamp`, `dataset_version`, `random_seed`
  (added automatically)
- whatever the caller passes in: model name, hyperparameters, CV scores,
  test-set metrics, feature subset, etc.

This is a deliberately low-tech substitute for MLflow: no server, nothing
to install, and the JSONL files are plain text — easy to `grep`, diff in a
pull request, or load into pandas (`pd.read_json(path, lines=True)`).

## Migrating to DVC later

If the dataset grows past "one CSV checked into git" (multiple raw sources,
a remote store, large files), the natural next step is:

```bash
pip install dvc
dvc init
dvc add data/clean_data.csv
git add data/clean_data.csv.dvc .gitignore
```

and pointing `dvc remote` at wherever the data should live. The
`dataset_version` hash scheme above maps directly onto DVC's own
content-addressed hashing, so existing experiment log entries stay
meaningful after the switch.

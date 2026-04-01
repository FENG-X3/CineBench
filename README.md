# CineBench

Public release of the CineBench benchmark: bilingual (Chinese/English) tables, video clips, and an evaluation pipeline.

## Contents

- `AI/`: AI-generated clips (~0.42 GB, 71 files).
- `movie/`: movie clips (~2.71 GB total, 375 files; flat folder).
- Root Excel splits: `CineBench_*_train.xlsx`, `CineBench_*_test.xlsx` (test rows use `correct_choice = -1`).
- `pipeline/`: evaluation code; default annotations: `pipeline/CineBench/data/cb_en_train.json`.
- `LICENSE`, `.gitignore`.

## Quick start (evaluation)

```bash
cd pipeline
python eval.py --model qwen --annotation_file cb_en_train.json --max_num_frames 16 --seed 42
```

See `pipeline/README.md` for dependencies and API keys.

## GitHub push and the 2 GiB pack limit

GitHub rejects a single receive pack larger than about **2 GiB**. This repository is split into **five commits** (code first, then `AI/`, then `movie/` in three size-limited batches) so each push uploads a smaller pack.

**Push in order** (advance `master` one commit at a time). List commits from oldest to newest:

```bash
git rev-list --reverse HEAD
```

Then push each hash in that list, one line at a time (use `-u` only on the first line):

```bash
git push -u origin <oldest_sha>:refs/heads/master
git push origin <next_sha>:refs/heads/master
# ... repeat until the newest sha
```

If `master` on the remote already points elsewhere and you intend to replace it with this history, use `--force` only when you understand that it overwrites the remote branch.

## Citation

If you use CineBench, please cite the corresponding paper once publicly released.

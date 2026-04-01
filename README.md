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

### After pushing: did anything actually fail?

From a healthy log, each step should end with `To github.com:...` and `<old>..<new>  <sha> -> master`. The line `Everything up-to-date` often appears because the same `git push` was run twice in one paste block; it is not an error.

Verify that the remote caught up with your laptop:

```bash
git fetch origin
git rev-parse HEAD
git rev-parse origin/master
```

The two SHAs should match (e.g. both `39d24e9...`).

### If a step fails mid-upload

Messages like `Connection reset by peer`, `Broken pipe`, or `unexpected disconnect` mean the network dropped during upload. **Re-run the same** `git push origin <that_commit_sha>:refs/heads/master` command; Git only sends missing objects.

### GitHub “large file” warnings

Warnings such as “larger than 50 MB” are **recommendations**, not a failed push. GitHub blocks individual blobs **≥ 100 MB**; your reported files (~56 MB) are still accepted. For a cleaner long-term setup, consider [Git LFS](https://git-lfs.github.com/).

## Citation

If you use CineBench, please cite the corresponding paper once publicly released.

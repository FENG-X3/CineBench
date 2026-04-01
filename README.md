# CineBench

`CineBench` is a bilingual (Chinese/English) video aesthetic benchmark designed for evaluating multimodal large models on cinematic understanding tasks.

## Repository contents

- `AI/`: AI-generated video clips used in benchmark items.
- `movie/`: movie video clips used in benchmark items.
- `CineBench_zh.xlsx` and `CineBench_en.xlsx`: bilingual benchmark tables.
- `zh_en_map.json`: Chinese-English mapping metadata.
- `标注结果/`: annotation and merged benchmark results.
- `pipeline/`: evaluation pipeline for model inference and scoring.
- `CineBench005.pdf`: paper draft/manuscript for submission.

## Quick start (evaluation)

```bash
cd pipeline
python eval.py --model qwen --annotation_file cb_zh.json --max_num_frames 16 --seed 42
```

See `pipeline/README.md` for full dependency and API-key configuration details.

## Notes for reviewers

- The benchmark is provided in both Chinese and English.
- Video assets are organized by source category (`AI` and `movie`).
- Evaluation scripts are cleaned for reproducibility and require API keys via environment variables only.

## Citation

If you use CineBench, please cite the corresponding paper once publicly released.

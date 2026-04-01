## CineBench Evaluation Pipeline

Run all commands from the `pipeline` directory.

### Environment

- Python 3.10+
- Recommended: CUDA-enabled PyTorch for faster video processing

### Required packages

- torch
- torchvision
- torchaudio
- numpy
- pandas
- pillow
- decord
- openai
- tqdm
- imageio
- imageio-ffmpeg
- openpyxl
- zai-sdk
- alibabacloud-oss-v2

### API keys

Set keys according to the model you use:

- `OR_API_KEY` for OpenRouter-based models (`gpt`, `gemini`, `internvl`)
- `ALI_API_KEY` and OSS credentials for `qwen`
- `Z_API_KEY` for `glm`
- `ARK_API_KEY` for `seed`

### Run evaluation

```bash
python eval.py --model qwen --annotation_file cb_en_train.json --max_num_frames 16 --seed 42
```

Outputs are written to `pipeline/results/<date>/<time>/`.

### Build train/test split (VLA env)

```bash
conda run -n VLA python split_benchmark.py
```

This creates:
- Root benchmark files: `CineBench_en_train.xlsx`, `CineBench_en_test.xlsx`, `CineBench_zh_train.xlsx`, `CineBench_zh_test.xlsx`
- Pipeline JSON files: `CineBench/data/cb_en_train.json`, `CineBench/data/cb_en_test.json`

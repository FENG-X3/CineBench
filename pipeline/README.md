## CineBench Evaluation Pipeline

## 中文说明

该目录提供 CineBench 的评测脚本与模型适配器。  
默认流程是：读取训练集标注文件、进行统一抽帧、调用模型作答、输出评测结果表格。

### 1) 环境准备

- Python 3.10+
- 建议使用支持 CUDA 的 PyTorch（可选）
- 你可以使用任意 Python 环境管理方式（conda / venv / system python）

### 2) 依赖安装

```bash
pip install torch torchvision torchaudio numpy pandas pillow decord openai tqdm imageio imageio-ffmpeg openpyxl zai-sdk alibabacloud-oss-v2
```

### 3) 配置 API Key（按所选模型）

- `OR_API_KEY`：`gpt` / `gemini` / `internvl`
- `ALI_API_KEY` + OSS 凭证：`qwen`
- `Z_API_KEY`：`glm`
- `ARK_API_KEY`：`seed`

### 4) 运行评测

```bash
python eval.py --model qwen --annotation_file cb_en_train.json --max_num_frames 16 --seed 42
```

结果输出到：`pipeline/results/<date>/<time>/`

### 5) 重新生成训练/测试拆分

```bash
python split_benchmark.py
```

会生成：
- 根目录表格：`CineBench_en_train.xlsx`, `CineBench_en_test.xlsx`, `CineBench_zh_train.xlsx`, `CineBench_zh_test.xlsx`
- 评测 JSON：`CineBench/data/cb_en_train.json`, `CineBench/data/cb_en_test.json`

---

## English Guide

This folder contains the evaluation scripts and model adapters for CineBench.

### 1) Environment

- Python 3.10+
- CUDA-enabled PyTorch is recommended (optional)
- Any environment manager is fine (conda / venv / system python)

### 2) Install dependencies

```bash
pip install torch torchvision torchaudio numpy pandas pillow decord openai tqdm imageio imageio-ffmpeg openpyxl zai-sdk alibabacloud-oss-v2
```

### 3) Set API keys (by model)

- `OR_API_KEY` for `gpt`, `gemini`, `internvl`
- `ALI_API_KEY` + OSS credentials for `qwen`
- `Z_API_KEY` for `glm`
- `ARK_API_KEY` for `seed`

### 4) Run evaluation

```bash
python eval.py --model qwen --annotation_file cb_en_train.json --max_num_frames 16 --seed 42
```

Outputs are written to `pipeline/results/<date>/<time>/`.

### 5) Regenerate train/test split

```bash
python split_benchmark.py
```

This creates:
- Root benchmark tables: `CineBench_en_train.xlsx`, `CineBench_en_test.xlsx`, `CineBench_zh_train.xlsx`, `CineBench_zh_test.xlsx`
- Evaluation JSON files: `CineBench/data/cb_en_train.json`, `CineBench/data/cb_en_test.json`

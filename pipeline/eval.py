import os
import re
import sys
import argparse
from datetime import datetime

from tqdm import tqdm
import numpy as np
import pandas as pd

from CineBench.cinebench.cinebench_dataset import CineBenchDataset
from models.model_loader import load_model


def random_sample(dataset, limit=None):
    """Random sample over the full dataset."""
    indices = np.arange(len(dataset))
    np.random.shuffle(indices)
    if limit is not None:
        eval_indices = indices[:limit]
    else:
        eval_indices = indices
    return eval_indices

def sample_by_category(annotations, limit=None):
    """Sample items by high-level category weights."""
    weights = {'Cinematography': 1, 'Lighting': 1, 'Color': 1, 'Emotional Cue': 1}

    category_indices = {category: [] for category in weights.keys()}
    categories = annotations['question_category']
    for i, category in categories.items():
        category_indices[category].append(i)

    total_weight = sum(weights.values())
    num_samples_per_category = {
        category: int(np.floor((weight / total_weight) * limit))
        for category, weight in weights.items()
    }

    remaining_samples = limit - sum(num_samples_per_category.values())
    if remaining_samples > 0:
        sorted_categories = sorted(weights.keys(), key=lambda x: weights[x], reverse=True)
        for i in range(remaining_samples):
            category_to_add = sorted_categories[i % len(sorted_categories)]
            num_samples_per_category[category_to_add] += 1

    eval_indices = []
    for category, num_samples in num_samples_per_category.items():
        available_indices = category_indices[category]

        if num_samples > len(available_indices):
            raise ValueError(f"{category} has not enough samples")
        else:
            shuffled_cat_indices = np.random.permutation(available_indices)
            eval_indices.extend(shuffled_cat_indices[:num_samples])

    eval_indices = np.random.permutation(eval_indices)

    return eval_indices

def sample_by_label(annotations):
    """Sample a fixed number from each fine-grained label."""
    sampling_rules = {
        'Cinematography': 20,
        'Lighting': 20,
        'Color': 20,
        'Emotional Cue': 20
    }

    main_categories = annotations['question_category']
    sub_categories = annotations['question']

    subcategory_indices = {}
    subcategory_to_main_category = {}

    for i, main_category in main_categories.items():
        sub_category = sub_categories[i]

        if sub_category not in subcategory_indices:
            subcategory_indices[sub_category] = []
            subcategory_to_main_category[sub_category] = main_category
        subcategory_indices[sub_category].append(i)

    eval_indices = []
    for sub_category, indices in subcategory_indices.items():
        main_category = subcategory_to_main_category[sub_category]

        num_to_sample = sampling_rules[main_category]

        if num_to_sample > len(indices):
            num_to_sample = len(indices)
        shuffled_indices = np.random.permutation(indices)
        eval_indices.extend(shuffled_indices[:num_to_sample])

    eval_indices = np.random.permutation(eval_indices)

    return eval_indices

def sample(annotations):
    """Movie: per-label sampling; AI: per-category weighted sampling."""
    movie_annotations = annotations[annotations['video_category'] == 'Movie']
    ai_annotations = annotations[annotations['video_category'] == 'AI']

    movie_indices = sample_by_label(movie_annotations)
    ai_indices = sample_by_category(ai_annotations, limit=200)    

    eval_indices = list(movie_indices) + list(ai_indices)
    eval_indices = np.random.permutation(eval_indices)

    return eval_indices



def main():
    parser = argparse.ArgumentParser(description="Evaluate a model on CineBench.")
    parser.add_argument("--model", type=str, default="qwen", help="Model alias defined in models/model_loader.py")
    parser.add_argument("--data_path", type=str, default="CineBench/data", help="Dataset root directory")
    parser.add_argument("--annotation_file", type=str, default="cb_en_train.json", help="Training-set annotation JSON filename")
    parser.add_argument("--max_num_frames", type=int, default=16, help="Number of sampled frames per video")
    parser.add_argument("--output_dir", type=str, default="results", help="Directory for output xlsx files")
    parser.add_argument("--limit", type=int, default=None, help="Optional limit for sampled items")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    experiment_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    np.random.seed(args.seed)

    model = load_model(args.model)

    dataset = CineBenchDataset(
        data_path=args.data_path,
        annotation_file=args.annotation_file,
        max_num_frames=args.max_num_frames
    )

    try:
        eval_indices = sample(dataset.annotations)
    except Exception as e:
        print(e)
        sys.exit(1)

    current_time = datetime.now()
    date_str = current_time.strftime("%Y-%m-%d")
    time_str = current_time.strftime("%H-%M-%S")
    base_dir = os.path.join(args.output_dir, date_str, time_str)
    os.makedirs(base_dir, exist_ok=True)

    result_path = os.path.join(base_dir, f"{model.name.split('/')[-1]}_{args.max_num_frames}.xlsx")

    results = []
    for i in tqdm(eval_indices, desc=f"{model.name.split('/')[-1]}: "):
        data = dataset[i]

        inputs = data["inputs"]

        try:
            output = model(inputs)
            print(output)
            match = re.findall(r'[A-E]', output.upper())
            answer = match[-1] if match else ""
            print(answer)
            answer = ord(answer) - ord('A') + 1 if 'A' <= answer <= 'Z' else "N/A"

            result = {
                "video_id": data["di"]["video_id"],
                "id": data["di"]["id"],
                "correct_choice": data["di"]["correct_choice"],
                "question": data["di"]["question"],
                **{f"option{i}": (data["di"]["candidates"][i-1] if i-1 < len(data["di"]["candidates"]) else "N/A") for i in range(1, 6)},
                "question_category": data["di"]["question_category"],
                "video_category": data["di"]["video_category"],
                "answer": answer,
                "is_correct": 1 if answer == data["di"]["correct_choice"] else 0,
                "model": model.name.split('/')[-1],
                "seed": args.seed,
                "max_num_frames": args.max_num_frames,
                "experiment_time": experiment_time
            }
            results.append(result)

            df = pd.DataFrame(results)
            df.to_excel(result_path, index=False, engine='openpyxl')
        except Exception as e:
            print(e)
    df = pd.DataFrame(results)
    df.to_excel(result_path, index=False, engine='openpyxl')


if __name__ == "__main__":
    main()




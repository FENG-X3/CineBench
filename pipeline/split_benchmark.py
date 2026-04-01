import os
import numpy as np
import pandas as pd


def to_json_records(df: pd.DataFrame, out_path: str) -> None:
    out = df.copy()
    option_cols = [f"option{i}" for i in range(1, 6)]
    out["candidates"] = out[option_cols].values.tolist()
    out = out.drop(columns=option_cols)
    out = out.where(pd.notna(out), None)
    out.to_json(out_path, orient="records", force_ascii=False, indent=2)


def split_by_category(df: pd.DataFrame, categories: list[str], seed: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    prefix = df["video_id"].astype(str).str.extract(r"^([A-Za-z]+)")[0]
    rng = np.random.default_rng(seed)
    test_mask = np.zeros(len(df), dtype=bool)

    for cat in categories:
        idx = np.where(prefix.to_numpy() == cat)[0]
        if len(idx) == 0:
            continue
        rng.shuffle(idx)
        test_mask[idx[: len(idx) // 2]] = True

    train_df = df.loc[~test_mask].copy()
    test_df = df.loc[test_mask].copy()
    return train_df, test_df


def main() -> None:
    root = r"f:\CVPR2026\CineBench"
    en_path = os.path.join(root, "CineBench_en.xlsx")
    zh_path = os.path.join(root, "CineBench_zh.xlsx")

    en = pd.read_excel(en_path)
    zh = pd.read_excel(zh_path)

    categories = ["AI", "JK", "OP", "DK", "GF", "SL", "TT"]
    train_en, test_en = split_by_category(en, categories, seed=42)
    train_zh, test_zh = split_by_category(zh, categories, seed=42)

    test_en["correct_choice"] = -1
    test_zh["correct_choice"] = -1

    train_en.to_excel(os.path.join(root, "CineBench_en_train.xlsx"), index=False)
    test_en.to_excel(os.path.join(root, "CineBench_en_test.xlsx"), index=False)
    train_zh.to_excel(os.path.join(root, "CineBench_zh_train.xlsx"), index=False)
    test_zh.to_excel(os.path.join(root, "CineBench_zh_test.xlsx"), index=False)

    outdir = os.path.join(root, "pipeline", "CineBench", "data")
    os.makedirs(outdir, exist_ok=True)
    # Keep pipeline JSON files English-only.
    to_json_records(train_en, os.path.join(outdir, "cb_en_train.json"))
    to_json_records(test_en, os.path.join(outdir, "cb_en_test.json"))

    print(f"en_train={len(train_en)} en_test={len(test_en)}")
    print(f"zh_train={len(train_zh)} zh_test={len(test_zh)}")


if __name__ == "__main__":
    main()

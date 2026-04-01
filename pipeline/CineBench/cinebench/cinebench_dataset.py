import pandas as pd
from torch.utils.data import Dataset
import os
from decord import VideoReader, cpu
from PIL import Image
import torch
import json


def load_video(video_file, duration, max_num_frames=16):  # max_num_frames: 
    """"""
    # from decord import VideoReader
    #  ctx=cpu(0): CPU num_threads=1: 
    vr = VideoReader(video_file, ctx=cpu(0), num_threads=1)
    #  ()
    fps = vr.get_avg_fps()
    #  
    total_valid_frames = int(duration * fps)
    # 
    # num_frames = min(max_num_frames, int(duration))
    num_frames = max_num_frames

    # 
    # :  total_valid_frames / num_frames 
    frame_indices = [int(total_valid_frames / num_frames) * i for i in range(num_frames)]

    # 
    frames = vr.get_batch(frame_indices)
    # 
    if isinstance(frames, torch.Tensor):
        frames = frames.numpy()
    else:
        frames = frames.asnumpy()

    # PIL.Image(RGB)
    # 
    return [Image.fromarray(fr).convert("RGB") for fr in frames]


class CineBenchDataset(Dataset):
    def __init__(self,
                 data_path,  # 
                 annotation_file,  # json cb.json
                 max_num_frames=16,  # 
                 ):
        super().__init__()
        self.data_path = data_path

        self.annotations = pd.read_json(os.path.join(data_path, annotation_file))

        with open(os.path.join(data_path, annotation_file), 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self.max_num_frames = max_num_frames

    def __getitem__(self, index):
        # 
        di = self.data[index]

        # 
        # if self.max_num_frames == 0:
        #     ### No subtitles, no frames
        #     inputs = []
        #     inputs += ["Question: " + di["question"]]
        #     # inputs += [". ".join([chr(ord("A") + i), candidate]) for i, candidate in enumerate(di["candidates"])]
        #     inputs += [f"({chr(ord('A') + i)}) {candidate}" for i, candidate in enumerate(di["candidates"])]
        #     # inputs += ["Answer with the option's letter from the given choices directly."]
        #     return {"inputs": inputs, "correct_choice": chr(ord("A") + di.get("correct_choice", -1)), "di": di}

        # 
        frames = load_video(os.path.join(self.data_path, di["video_path"]), di["duration"],
                                              max_num_frames=self.max_num_frames)
        # frames = load_video(os.path.join(self.data_path, di["video_path"]).replace('\\', '/'), di["duration"], 
        #                                       max_num_frames=self.max_num_frames)

        inputs = frames
        ##### YOU MAY MODIFY THE FOLLOWING PART TO ADAPT TO YOUR MODEL #####
        # 
        inputs += ["Question: " + di["question"]]
        # inputs += [": " + di["question"]]
        # 
        # inputs += [". ".join([chr(ord("A") + i), candidate]) for i, candidate in enumerate(di["candidates"])]
        inputs += [f"({chr(ord('A') + i)}) {candidate}" for i, candidate in enumerate(di["candidates"])]
        # prompt
        # inputs += ["Answer with the option's letter from the given choices directly."]
        ##### YOU MAY MODIFY THE PREVIOUS PART TO ADAPT TO YOUR MODEL #####

        ##### CORRECT CHOICE WILL BE "@" FOR TEST SET SAMPLES #####
        return {"inputs": inputs, "di": di}

    def __len__(self):
        return len(self.data)



if __name__ == "__main__":
    # 
    dataset = CineBenchDataset("./Cinebench/data", "cb_zh.json")
    for i in range(3):
        # print([ele for ele in dataset[i]["inputs"] if not isinstance(ele, str)])
        print(dataset[i]["inputs"])
        # print(dataset[i]['di'].keys())
        # print(dataset[i]['di']['correct_choice'])
        # print(dataset[i]['di']['id'])

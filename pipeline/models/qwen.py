import os
import time

from openai import OpenAI
from PIL import Image
from models.utils import convert_frames_to_video, encode_video, upload_to_oss
import alibabacloud_oss_v2 as oss


class Qwen:
    def __init__(self):
        # fps=1
        self.name = "qwen3-vl-plus-2025-12-19"
        # self.name = "qwen3-vl-plus-2025-09-23"
        # self.name = "qwen3-vl-flash-2025-10-15"
        # self.name = "qwen3-vl-235b-a22b-thinking"
        # self.name = "qwen3-vl-8b-thinking"
        api_key = os.getenv("ALI_API_KEY")
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )

        # ，
        credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
        # SDK，
        cfg = oss.config.load_default()
        cfg.credentials_provider = credentials_provider
        # ：Region（）
        # Region ID，1（），Regioncn-hangzhou，SDKRegionHTTPS
        cfg.region = 'cn-beijing'
        # OSS
        self.client_oss = oss.Client(cfg)


    def __call__(self, inputs):
        # 
        frames = [item for item in inputs if isinstance(item, Image.Image)]
        text = [item for item in inputs if isinstance(item, str)]

        video = convert_frames_to_video(frames, fps=1)

        prompt = "\n".join(text + ["Answer using only a single option letter (A/B/C/D/E)."])
        print(prompt)

        try:
            response = self.client.chat.completions.create(
                model=self.name,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "video_url",
                                "video_url": {
                                    # "url": f"data:video/mp4;base64,{encode_video(video)}",
                                    "url": upload_to_oss(self.client_oss, self.name, video),
                                },
                                "fps": 1
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ],
                # alibailian fps=2
                extra_body = {
                    'enable_thinking': True,  # False
                },
            )
            return response.choices[0].message.content
        except Exception as e:
            print(e)
            raise


if __name__ == '__main__':
    pass




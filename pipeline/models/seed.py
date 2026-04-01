import os
from openai import OpenAI
from PIL import Image
from models.utils import convert_frames_to_video, encode_video


class Seed:
    def __init__(self):
        # fps=1
        self.name = "doubao-seed-1-8-251228"
        # self.name = "doubao-Seed-1.6-vision-250815"
        api_key = os.getenv("ARK_API_KEY")
        self.client = OpenAI(
            # ，
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            api_key=api_key
        )

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
                                    "url": f"data:video/mp4;base64,{encode_video(video)}",
                                    "fps": 1  # 1 0.2~5
                                }
                            },
                            {
                                "type": "text", 
                                "text": prompt
                            }
                        ],
                    }
                ],
                extra_body={
                    "thinking": {
                        "type": "enabled",  # enabled
                    }
                },
            )
            return response.choices[0].message.content
        except Exception as e:
            print(e)
            raise


if __name__ == '__main__':
    pass

    # print(response.choices[0])



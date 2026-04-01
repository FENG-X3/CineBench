import os
from openai import OpenAI
from PIL import Image
from models.utils import convert_frames_to_video, encode_video


class InternVL:
    def __init__(self):
        # fps=?
        self.name = "opengvlab/internvl3-78b"
        api_key = os.getenv("OR_API_KEY")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
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
                extra_body={},
                model=self.name,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "video_url",
                                "video_url": {
                                    "url": f"data:video/mp4;base64,{encode_video(video)}",
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            print(e)
            raise


if __name__ == '__main__':
    pass

    # import requests
    # url = "https://openrouter.ai/api/v1/key"
    # headers = {"Authorization": "Bearer <YOUR_OR_API_KEY>"}
    # response = requests.get(url, headers=headers)
    # print(response.json())




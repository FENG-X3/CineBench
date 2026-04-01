import os
from PIL import Image
from zai import ZhipuAiClient
from models.utils import convert_frames_to_video, encode_video


class GLM:
    def __init__(self):
        # fps=?
        self.name = "glm-4.6v-106B"
        # self.name = "glm-4.5v-106B"
        api_key = os.getenv("Z_API_KEY")
        self.client = ZhipuAiClient(api_key=api_key)

    def __call__(self, inputs):
        # 
        frames = [item for item in inputs if isinstance(item, Image.Image)]
        text = [item for item in inputs if isinstance(item, str)]

        video = convert_frames_to_video(frames, fps=1)

        prompt = "\n".join(text + ["Answer using only a single option letter (A/B/C/D/E)."])
        # prompt = "\n".join(text + ["，<|begin_of_box|>X<|end_of_box|>，（）"])
        print(prompt)

        try:
            response = self.client.chat.completions.create(
                model="glm-4.6v",
                # model="glm-4.5v",
                messages=[
                    {
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
                        ],
                        "role": "user"
                    }
                ],
                thinking={
                    "type": "enabled"  # enabled disabled
                }
            )
            return response.choices[0].message.content
        except Exception as e:
            print(e)
            raise


if __name__ == '__main__':
    pass

    # import zai
    # print(zai.__version__)

    # print(response.choices[0].message)


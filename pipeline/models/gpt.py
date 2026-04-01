import os
from openai import OpenAI
from PIL import Image
from models.utils import encode_image


class GPT:
    def __init__(self):
        self.name = "openai/gpt-5.2"
        api_key = os.getenv("OR_API_KEY")
        if not api_key:
            raise EnvironmentError("Missing OR_API_KEY environment variable.")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

    def __call__(self, inputs):
        # 
        frames = [item for item in inputs if isinstance(item, Image.Image)]
        text = [item for item in inputs if isinstance(item, str)]

        prompt = "\n".join(text + ["Answer with the option's letter from the given choices directly.Single choice:"])
        print(prompt)

        try:
            response = self.client.chat.completions.create(
                model=self.name,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            *[{
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{encode_image(frame)}",
                                }
                            } for frame in frames],
                            {
                                "type": "text",
                                "text": prompt
                            },
                        ]
                    }
                ],
                extra_body={
                    "reasoning": {
                        "enabled": True
                    }
                }
            )
            return response.choices[0].message.content
        except Exception as e:
            print(e)
            raise


if __name__ == '__main__':
    pass

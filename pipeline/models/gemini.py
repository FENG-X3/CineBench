import os
from openai import OpenAI
from PIL import Image
from models.utils import convert_frames_to_video, encode_video


class Gemini:
    def __init__(self):
        # fps=1
        # self.name = "google/gemini-3-pro-preview"
        self.name = "google/gemini-3-flash-preview"
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

        video = convert_frames_to_video(frames, fps=1)

        # prompt = "\n".join(text + ["Answer with the option's letter from the given choices directly."])
        prompt = "\n".join(text + [
                    "--------------------------------------------------\n"
                    "CRITICAL INSTRUCTION:\n"
                    "You are an automated evaluation system. Your task is to output the correct option key.\n"
                    "1. Analyze the content.\n"
                    "2. Select the best answer.\n"
                    "3. Output ONLY the single capital letter (A, B, C, D, or E).\n"
                    "4. STRICTLY NO EXPLANATION. NO REASONING. NO EXTRA WORDS.\n"
                    "--------------------------------------------------\n"
                    "Final Answer:"
                ])
        print(prompt)

        try:
            # OpenRouter
            response = self.client.chat.completions.create(
                model=self.name,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_video",
                                "video_url": {
                                    "url": f"data:video/mp4;base64,{encode_video(video)}"
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ],
                extra_body={"reasoning": {"enabled": True}}  # 
            )
            return response.choices[0].message.content
        except Exception as e:
            print(e)
            raise


if __name__ == '__main__':
    pass

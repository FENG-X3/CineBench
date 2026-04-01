from .qwen import Qwen


def load_model(model_name):
    if model_name == "qwen":
        return Qwen()
    if model_name == "qwen2":
        from .qwen2 import Qwen2
        return Qwen2()
    elif model_name == "seed":
        from .seed import Seed
        return Seed()
    elif model_name == "glm":
        from .glm import GLM
        return GLM()
    elif model_name == "internvl":
        from .internvl3_5_8b.invernvl import InternVL
        return InternVL()
    # elif model_name == "video_chat2":
    #     from .video_chat2 import VideoChat2
    #     return VideoChat2()
    elif model_name == "gpt":
        from .gpt import GPT
        return GPT()
    elif model_name == "gemini":
        from .gemini import Gemini
        return Gemini()
    return Qwen()
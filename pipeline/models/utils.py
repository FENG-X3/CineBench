import io
import base64
import numpy as np
import imageio
import alibabacloud_oss_v2 as oss
import tempfile


def convert_frames_to_video(frames, fps):
    # 
    video_buffer = io.BytesIO()

    with imageio.get_writer(
            video_buffer,
            format='mp4',
            fps=fps,
            codec='libx264',
            output_params=['-pix_fmt', 'yuv420p'],
            ffmpeg_log_level='error', 
            macro_block_size=1
    ) as writer:
        for frame in frames:
            np_frame = np.array(frame)
            writer.append_data(np_frame)

    # 
    return video_buffer.getvalue()

def encode_video(video):
    return base64.b64encode(video).decode('utf-8')

def encode_image(image):
    buffer = io.BytesIO()
    image.convert('RGB').save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def upload_to_oss(client, model_name, video):
    # ，、
    result = client.put_object(oss.PutObjectRequest(
        bucket="java-ai-wxe",
        key=f"{model_name}/temp_video.mp4",
        body=video,
    ))

    return f"https://java-ai-wxe.oss-cn-beijing.aliyuncs.com/{model_name}/temp_video.mp4"

def convert_frames_to_temp_video(frames, fps):
    """PIL Imagemp4"""
    import cv2
    if not frames:
        return None

    # 
    width, height = frames[0].size

    # 
    temp = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
    temp_path = temp.name
    temp.close()

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_path, fourcc, fps, (width, height))

    # 
    for frame in frames:
        open_cv_image = np.array(frame)
        open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

        out.write(open_cv_image)

    out.release()

    return temp_path



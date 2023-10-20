import os
from PIL import Image
from cv2 import VideoWriter, imread, VideoWriter_fourcc


def image_to_video(imgs_path, video_path, fps=60):
    images = os.listdir(imgs_path)
    images.remove('.gitignore')
    img_size = Image.open(imgs_path + images[0]).size
    fourcc = VideoWriter_fourcc(*'mp4v')
    video_writer = VideoWriter(video_path, fourcc, fps, img_size)
    for i in range(len(images)):
        path = imgs_path + str(i) + '.png'
        frame = imread(path)
        video_writer.write(frame)
    video_writer.release()

image_to_video('screenshots/', 'test.mp4')

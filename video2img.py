import os
import numpy
import pandas as pd


def command(start_time: str, file_name: str, duration: float, frames: float, index: int, series: int):
    return "ffmpeg -ss {} -i {} -t {:.2f} -r {:.3f} -f image2 -qscale:v 2 result/{}-{}-%3d.jpg" \
        .format(start_time, file_name, duration, frames / duration, series, index)


def list_video():
    file_name = [videos for videos in os.listdir() if videos.endswith('.mp4')]  # 得到所有文件的列表
    df = pd.DataFrame(file_name, columns=['file_name'])
    df.to_excel('video.xlsx')


def ffmpeg_execute():
    df = pd.read_excel('video_label.xlsx', index_col=0)
    command_list = []
    for index, rows in df.iterrows():
        if rows['start_time_1'] != "manual" and not pd.isnull(rows['start_time_1']):
            command_list.append(
                command(rows['start_time_1'], rows['file_name'], rows['duration_1'], rows['frames_1'], index, 0))
        command_list.append(
            command(rows['start_time_2'], rows['file_name'], rows['duration_2'], rows['frames_2'], index, 1))
    for ffmpeg_cmd in command_list:
        os.system(ffmpeg_cmd)


def train_test_div(n_videos=101, train_rate=0.8):
    xml_labeled = os.listdir('labels')
    image_labeled = []
    for i in xml_labeled:
        image_labeled.append(i[:-3] + "jpg")  # 修改已标注图片列表中的后缀为jpg
    print(image_labeled)
    train_n = numpy.random.choice(n_videos, int(n_videos * train_rate), replace=False)
    print(train_n)


if __name__ == '__main__':
    train_test_div()

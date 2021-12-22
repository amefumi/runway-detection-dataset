import os
import numpy
import pandas as pd
import re


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


def train_test_div(n_videos=101, train_rate=0.7):
    train_n = numpy.random.choice(n_videos, int(n_videos * train_rate), replace=False)  # 选取作为训练集的视频的序号
    print('Train Set No. (Total = {}) = '.format(len(train_n)), train_n)

    xml_labeled = os.listdir('labels')
    image_train = []
    image_train_far = []
    image_train_near = []
    image_test = []
    image_test_far = []
    image_test_near = []

    for i in xml_labeled:
        image_name = i[:-4]
        p_video = re.findall(r'-(.*?)-', i)
        if int(p_video[0]) in train_n:
            image_train.append(image_name)
            if i[0] == '0':
                image_train_far.append(image_name)
            else:
                image_train_near.append(image_name)
        else:
            image_test.append(image_name)
            if i[0] == '0':
                image_test_far.append(image_name)
            else:
                image_test_near.append(image_name)
    print(image_train)
    image_train_txt = open('train.txt', 'w')
    for i in image_train:
        image_train_txt.write(i + '\n')
    image_train_txt.close()

    print(image_train_far)
    image_train_far_txt = open('train_far.txt', 'w')
    for i in image_train_far:
        image_train_far_txt.write(i + '\n')
    image_train_far_txt.close()

    print(image_train_near)
    image_train_near_txt = open('train_near.txt', 'w')
    for i in image_train_near:
        image_train_near_txt.write(i + '\n')
    image_train_near_txt.close()

    print(image_test)
    image_test_txt = open('test.txt', 'w')
    for i in image_test:
        image_test_txt.write(i + '\n')
    image_test_txt.close()

    print(image_test_far)
    image_test_far_txt = open('test_far.txt', 'w')
    for i in image_test_far:
        image_test_far_txt.write(i + '\n')
    image_test_far_txt.close()

    print(image_test_near)
    image_test_near_txt = open('test_near.txt', 'w')
    for i in image_test_near:
        image_test_near_txt.write(i + '\n')
    image_test_near_txt.close()


if __name__ == '__main__':
    train_test_div()

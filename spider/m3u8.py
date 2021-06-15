import requests
from moviepy.editor import *

# 绝对路径
work_dir = os.path.dirname(os.path.abspath(__file__))
# 把当前路径切换到文件所在的路径
os.chdir(work_dir)

video_path = '../data/video/'


# 获取地址
def get_path():
    url = 'https://vod.bunediy.com/20210430/36JdJMQn/index.m3u8'
    resp = requests.get(url).text
    print(resp)

    resp = resp.split("\n")
    count = 1
    for i in resp:
        if "https" in i:
            print(i)
            down("../data/video/" + str(count) + ".mp4", i)
            count += 1


# 获取分片
def down(name, v_url):
    down_res = requests.get(url=v_url, stream=True)
    with open(name, "ab") as code:
        code.write(down_res.content)
        code.close()


# 合并
def combine():
    tem_list = [VideoFileClip(f'{video_path}' + str(j) + ".mp4") for j in range(1, 51)]
    video = concatenate_videoclips(tem_list)
    video.write_videofile(f"{video_path}trj3.mp4")
    exit()

    big_list = []
    # 以50个为界限进行合并，1618/50=33（取整），最后再将33个大片段
    for i in range(1, 1618, 50):
        print(i)
        if i < 1600:
            tem_list = [VideoFileClip(f'{video_path}' + str(j) + ".mp4") for j in range(i, i + 50)]
        else:
            tem_list = [VideoFileClip(f'{video_path}' + str(j) + ".mp4") for j in range(i, 1619)]

        video_tem = concatenate_videoclips(tem_list)
        big_list.append(video_tem)

    video = concatenate_videoclips(big_list)
    video.write_videofile(f"{video_path}trj3.mp4")


def main():
    # get_path()
    combine()


if __name__ == '__main__':
    main()

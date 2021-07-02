#基于的基础镜像
FROM python:3.7

#代码添加到code文件夹，后面可以通过进入容器中看的
ADD ./py /code

# 设置code文件夹是工作目录
WORKDIR /code

# 安装支持
RUN pip install -r requirements.txt

#当容器启动时，使用python3执行指定路径的py脚本
CMD ["python3", "/code/venv/Include/job.py"]
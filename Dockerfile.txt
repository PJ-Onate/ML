FROM debian:11-slim

#COPY . /tmp

RUN apt-get update \
&& apt-get -y upgrade \
&& apt install -y curl \
&& apt-get install -y python3 \
&& apt-get install -y python3-tk \
&& apt-get install ffmpeg libsm6 libxext6  -y \
&& apt-get install -y x11-xserver-utils 

RUN export DISPLAY=$DISPLAY
RUN apt-get install nano
RUN pip install mysql-connector-python
#RUN xhost +


RUN apt install -y python3-pip
RUN python3 -m pip install --upgrade pip
RUN apt-get install -y git

#DEPENDENCIAS A UTILIZAR

RUN pip install opencv-python \
&& pip install Pillow \
&& pip install imutils 
#&& pip install tkinter
#docker run -ti --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix <nombre-imagen>

CMD ["python3", "/tmp/main.py"]





#CMD {"/bin/bash"Tk


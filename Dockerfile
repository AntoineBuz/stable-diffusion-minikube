FROM nvidia/cuda:12.2.2-devel-ubuntu22.04

RUN apt update -y && apt upgrade -y
RUN apt install -y python3 python3-pip 
RUN python3 -m pip install --upgrade pip

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY config.json .
COPY dl_model.py .

RUN python3 dl_model.py

COPY . .

EXPOSE 7860

ENTRYPOINT ["python3", "main.py"]   
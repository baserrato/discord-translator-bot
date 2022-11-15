FROM ubuntu:20.04

WORKDIR /root

COPY bot.py .

RUN apt update && apt upgrade -y

RUN apt install vim -y 
RUN apt install pip -y
RUN apt install curl -y

RUN pip install pylint==2.15.2 && \
    pip install python-dotenv==0.21.0 && \
    pip install googletrans==4.0.0rc1 && \
    pip install discord.py==2.0.1 && \
    pip install requests==2.28.1

ENTRYPOINT ["./bot.py"]

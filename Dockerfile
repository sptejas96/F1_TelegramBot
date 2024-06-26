FROM registry.access.redhat.com/ubi9/ubi-minimal:latest
WORKDIR /home/F1TelegramBot/src
RUN microdnf -y install python39
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py
COPY 2024.json .
COPY f1telegrambot.py .
COPY requirements.txt .
COPY telegram_bot_token.json .
RUN pip install -r requirements.txt
CMD [ "python3", "f1telegrambot.py" ]

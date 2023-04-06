FROM python:3.9

WORKDIR /PromptHub

RUN git clone https://github.com/CODE-FOR/PromptHub-backend.git  /PromptHub/backend

WORKDIR /PromptHub/backend

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
RUN python manage.py makemigrations core
RUN python manage.py migrate

EXPOSE 8080
FROM public.ecr.aws/lambda/python:3.8

RUN yum install -y curl unzip fontconfig libX11 libXcomposite libXcursor libXdamage libXext libXi libXtst libXrandr libXScrnSaver libXrender libXss libxslt-devel libXtst liberation-fonts liberation-narrow-fonts liberation-sans-fonts liberation-serif-fonts pango
RUN curl -O https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
RUN yum install -y ./google-chrome-stable_current_x86_64.rpm
RUN yum install unzip -y
RUN wget https://chromedriver.storage.googleapis.com/112.0.5615.49/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/bin/chromedriver

RUN rm chromedriver_linux64.zip
RUN rm google-chrome-stable_current_x86_64.rpm

COPY requirements.txt /var/task/
RUN pip install -r requirements.txt

COPY src/ /var/task/

CMD ["app.handler"]
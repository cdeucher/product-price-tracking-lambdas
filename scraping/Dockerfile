FROM public.ecr.aws/lambda/python:3.8

RUN yum update -y
RUN yum install -y curl unzip fontconfig libX11 libXcomposite libXcursor libXdamage libXext libXi libXtst libXrandr libXScrnSaver libXrender libXss libxslt-devel libXtst liberation-fonts liberation-narrow-fonts liberation-sans-fonts liberation-serif-fonts pango
RUN yum install -y unzip bzip2 wget tar gzip


#RUN curl -O https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
#RUN yum install -y ./google-chrome-stable_current_x86_64.rpm
#RUN wget https://chromedriver.storage.googleapis.com/112.0.5615.49/chromedriver_linux64.zip
#RUN unzip chromedriver_linux64.zip
#RUN mv chromedriver /usr/bin/chromedriver
#RUN rm chromedriver_linux64.zip
#RUN rm google-chrome-stable_current_x86_64.rpm

RUN wget -O ~/FirefoxSetup.tar.bz2 "https://download.mozilla.org/?product=firefox-latest&os=linux64"
RUN tar xjf ~/FirefoxSetup.tar.bz2 -C /opt/
RUN ln -s /opt/firefox/firefox /usr/bin/firefox
RUN rm ~/FirefoxSetup.tar.bz2

RUN wget -O ~/geckodriver-v0.33.0-linux64.tar.gz "https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz"
RUN tar xzf ~/geckodriver-v0.33.0-linux64.tar.gz -C /opt/
RUN ln -s /opt/geckodriver /usr/bin/geckodriver
RUN rm ~/geckodriver-v0.33.0-linux64.tar.gz

COPY requirements.txt /var/task/
RUN pip install -r requirements.txt

COPY src/ /var/task/

RUN yum install -y gtk3 alsa-lib-devel dbus-glib-devel
RUN yum install -y which
RUN yum install -y \
    dbus-glib-devel-0.100-7.2.amzn2 \
    gtk2-devel-2.24.31-1.amzn2.0.2 \
    gtk3-devel-3.22.30-3.amzn2 \
    libXt-devel-1.1.5-3.amzn2.0.2 \
    llvm-devel-11.1.0-1.amzn2.0.2 \
    nasm-2.15.03-3.amzn2.0.1 \
    pango-devel-1.42.4-4.amzn2 \
    pulseaudio-libs-devel-10.0-3.amzn2.0.3
RUN yum install -y \
    dbus-glib-0.100-7.2.amzn2 \
    gtk3-3.22.30-3.amzn2 \
    libXt-1.1.5-3.amzn2.0.2 \
    xorg-x11-server-Xvfb-1.20.4-15.amzn2.0.2

CMD ["app.handler"]
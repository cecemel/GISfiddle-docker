FROM node:4
RUN git clone https://github.com/cecemel/GISfiddle.git
WORKDIR /GISfiddle
COPY ./default_config.json /GISfiddle/config/default.json
COPY ./start_node.sh /GISfiddle/start_node.sh
CMD ["/bin/bash", "start_node.sh"]

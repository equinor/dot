FROM tinkerpop/gremlin-server:3.6.2@sha256:b2ff682f4ab5705389d1c982675cc7e12b484184f07becba170098b1a4330a5e

USER root

COPY ./db/conf /opt/gremlin-server/conf
COPY ./db/scripts /opt/gremlin-server/scripts

RUN wget -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.2.5/dumb-init_1.2.5_x86_64
RUN chmod +x /usr/local/bin/dumb-init

ENTRYPOINT ["dumb-init", "--rewrite", "15:2", "--", "/docker-entrypoint.sh"]

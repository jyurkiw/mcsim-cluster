FROM alpine:latest

RUN apk update; apk add nano curl bash; mkdir scripts
COPY scripts /scripts
RUN chmod +x /scripts/*; \
    dos2unix /scripts/*
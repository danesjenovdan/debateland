#!/bin/bash

sudo docker login rg.fr-par.scw.cloud/parlasearch -u nologin -p $SCW_SECRET_TOKEN
sudo docker build -f debateland/Dockerfile debateland -t debateland:latest
sudo docker tag debateland:latest rg.fr-par.scw.cloud/djnd/debateland:latest
sudo docker push rg.fr-par.scw.cloud/djnd/debateland:latest

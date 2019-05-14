#!/usr/bin/env bash

docker build . -t py27cpu -f Dockerfile.py27cpu
docker tag py27cpu tinymind/base:py27-cpu
docker push tinymind/base:py27-cpu

docker build . -t py27gpu -f Dockerfile.py27gpu
docker tag py27gpu tinymind/base:py27-gpu
docker push tinymind/base:py27-gpu

docker build . -t py27gpu-cuda9 -f Dockerfile.py27gpu-cuda9
docker tag py27gpu-cuda9 tinymind/base:py27-gpu-cuda9
docker push tinymind/base:py27-gpu-cuda9

docker build . -t py27gpu-cuda91 -f Dockerfile.py27gpu-cuda91
docker tag py27gpu-cuda91 tinymind/base:py27-gpu-cuda91
docker push tinymind/base:py27-gpu-cuda91

docker build . -t py36cpu -f Dockerfile.py36cpu
docker tag py36cpu tinymind/base:py36-cpu
docker push tinymind/base:py36-cpu

docker build . -t py36gpu -f Dockerfile.py36gpu
docker tag py36gpu tinymind/base:py36-gpu
docker push tinymind/base:py36-gpu

docker build . -t py36gpu-cuda9 -f Dockerfile.py36gpu-cuda9
docker tag py36gpu-cuda9 tinymind/base:py36-gpu-cuda9
docker push tinymind/base:py36-gpu-cuda9

docker build . -t py36gpu-cuda91 -f Dockerfile.py36gpu-cuda91
docker tag py36gpu-cuda91 tinymind/base:py36-gpu-cuda91
docker push tinymind/base:py36-gpu-cuda91

docker build . -t py36gpu-cuda10 -f Dockerfile.py36gpu-cuda10
docker tag py36gpu-cuda10 tinymind/base:py36-gpu-cuda10
docker push tinymind/base:py36-gpu-cuda10
FROM nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04
LABEL author="TinyMind" website="www.tinymind.com" email="hello@tinymind.com"

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        curl \
        git \
        graphviz \
        g++ \
        libbz2-dev \
        libffi-dev \
        libfreeimage-dev \
        libfreetype6-dev \
        libgl1-mesa-dev \
        libglu1-mesa-dev \
        libhdf5-dev \
        libjpeg-dev \
        liblapack-dev \
        liblcms2-dev \
        libncurses5-dev \
        libncursesw5-dev \
        libopenblas-dev \
        libjpeg-dev \
        libpng-dev \
        libreadline-dev \
        libsqlite3-dev \
        libssl-dev \
        libtiff5-dev \
        libwebp-dev \
        libzmq3-dev \
        llvm \
        make \
        pkg-config \
        rsync \
        software-properties-common \
        unzip \
        vim \
        wget \
        xz-utils \
        zlib1g-dev \
        python3 \
        python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    rm get-pip.py

RUN pip --no-cache-dir install --upgrade \
        Pillow \
        h5py \
        ipykernel \
        jupyter \
        keras_applications \
        keras_preprocessing \
        matplotlib \
        mock \
        numpy \
        scipy \
        scikit-learn \
        pandas \
        mkl \
        pyyaml \
        enum34 \
        Cython \
        tinyenv

# Install TensorRT 5.0.2
RUN apt-get update && \
    apt-get install nvinfer-runtime-trt-repo-ubuntu1804-5.0.2-ga-cuda10.0 && \
    apt-get update && \
    apt-get install -y --no-install-recommends libnvinfer5 libnvinfer-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Link NCCL libray and header where the build script expects them.
RUN mkdir /usr/local/cuda/lib &&  \
    ln -s /usr/lib/x86_64-linux-gnu/libnccl.so.2 /usr/local/cuda/lib/libnccl.so.2 && \
    ln -s /usr/include/nccl.h /usr/local/cuda/include/nccl.h

# A link. I don't know it only need in build or similarly need in runtime. Add it.
RUN ln -s /usr/local/cuda/lib64/stubs/libcuda.so /usr/local/cuda/lib64/stubs/libcuda.so.1

# A env. Similary, I don’t know what to use.
ENV LD_LIBRARY_PATH /usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64:$LD_LIBRARY_PATH

# Override config in build user docker image.
COPY jupyter_notebook_config.py /etc/jupyter/jupyter_notebook_config.py

# Jupyter has issues with being run directly:
# https://github.com/ipython/ipython/issues/7062
COPY jupyter.sh /
RUN chmod +x /jupyter.sh

EXPOSE 8888

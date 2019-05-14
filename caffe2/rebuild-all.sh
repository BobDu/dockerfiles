declare -a versions=(
  "0.8-py27-cpu"
  "0.8-py27-gpu"
)

for i in "${versions[@]}"
do
   docker build . -t caffe2${i} -f Dockerfile.caffe2${i}
   docker tag caffe2${i} tinymind/caffe2:${i}
   docker push tinymind/caffe2:${i}
done

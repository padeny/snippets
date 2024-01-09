start() {
  docker run -itd --restart=always \
    --network="host" \
    --cpuset-cpus="0" \
    -m 1024m \
    --name calib_task \
    -v /etc/localtime:/etc/localtime \
    # -v 会自动在宿主机创建目录当目录不存在时
    --mount type=bind,source=/xxx,target=/usr/src/xxx,readonly \
    ${RuntimeImage}
}

#!/bin/bash
set -e
for d in $@; do
  find "$d" \
    ! \( \
      -group 1002 \
      -a -perm -g+rwX  \
    \) \
    -exec chgrp 1002 {} \; \
    -exec chmod g+rwX {} \;
  find "$d" \
    \( \
        -type d \
        -a ! -perm -6000  \
    \) \
    -exec chmod +6000 {} \;
done

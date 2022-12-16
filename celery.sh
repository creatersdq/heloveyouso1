#!/bin/bash
#执行shell脚本 sh ./celery_start.sh
echo "celery 脚本开始启动 --------"
job_comm='celery -A app.job.celery_app worker -l info'
# shellcheck disable=SC2034
if current_dir=$(
  # shellcheck disable=SC2046
  cd $(dirname "$0")
  pwd
)
then echo "获取当前路径:";echo"$current_dir"
else echo "获取当前路径异常"
fi

if parent_dir=$(
  # shellcheck disable=SC2046
  cd $(dirname "$0")
  # shellcheck disable=SC2103
  cd ..
  pwd
)
then echo "获取父级路径:";echo "$parent_dir"
else echo "获取父级路径异常"
fi

if echo "进入 脚本启动路径:";cd "$parent_dir"
then $job_comm
else echo "celery 脚本启动异常 --------"
fi

echo "celery 脚本关闭--------"




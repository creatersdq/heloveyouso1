#!/bin/sh
appName=gunicorn
appPid=0

getPid() {
    appPid=`ps -ef | grep ${appName} | grep -v grep | grep -v $0 | awk '{print $2}'`
}

startService() {
    if [[ ${appPid} -eq 0 ]];then
        echo "${appName} is not running.开始启动服务...."
        gunicorn  -c gunicorn_conf.py -D main:app  -k uvicorn.workers.UvicornWorker
        getPid
        echo "${appName} is running. pid=[${appPid}]."
    else
	getPid
    	echo "${appName} is running. pid=[${appPid}]"
    	exit 1
    fi
}

stopService() {
    getPid
    if [[ ${appPid} -eq 0 ]];then
    	echo "${appName} is not running..."
    else
    	kill -9 ${appPid}
    	echo "the proccess pid=[${appPid}] has been stopped."
    fi
}

restartService() {
    getPid
    if [[ ${appPid} -eq 0 ]];then
    	echo "${appName} is not running..."
    	exit 1
    else
    	stopService
    	sleep 5
    	getPid
    	if [[ -z ${appPid} ]];then
    	    startService

    	else
            kill -9 ${appPid}
    	    startService
    	fi
    	getPid
    	echo "${appPid} has been restarted. pid=[${appPid}]."
    fi
}

checkService() {
    getPid
    if [[ ${appPid} -eq 0 ]];then
        echo "${appName} is not running..."
    else
        echo "${appName} is running. pid=[${appPid}]."
    fi
}

serviceUsage() {
    echo "Usage: $0 start | stop | restart | status"
    exit 1
}

main() {
    if [[ $# -ne 1 ]];then
	serviceUsage
    else
        case $1 in
    	start)
    	    startService
            ;;
    	stop)
    	    stopService
    	    ;;
    	restart)
    	    restartService
     	    ;;
    	status)
    	    checkService
    	    ;;
    	*)
    	    serviceUsage
    	    ;;
        esac
    fi
}

main $@
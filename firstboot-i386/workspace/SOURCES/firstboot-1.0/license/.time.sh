#! /bin/bash

PRODUCT="$1"
WORK_DIR=`cd ${0%/*} && pwd`
SHELLNAME=${0#*/}
TIME_FILE="$WORK_DIR/${PRODUCT}.time"
LOG_FILE="$WORK_DIR/${PRODUCT}.log"

if [[ $# != 2 ]]; then
	echo "Usage: $SHELLNAME [product] {start|stop}"
	echo "Stop $PRODUCT license. Reason: Shell command error." >> $LOG_FILE
	exit 1
fi

import_into_timefile()
{
	grep "^$1" $TIME_FILE > /dev/null
	if [ $? -eq 0 ]; then
		sed -i "/$1/s/-*[0-9][0-9]*/$2/g" $TIME_FILE
	else
		echo -e "\n$1 $2" >> $TIME_FILE
	fi
}

start_license()
{
	TIME=`awk '/license/{print $2}' $TIME_FILE`
	if [ "$TIME" == "" ]; then
		echo "Stop $PRODUCT license. Reason: Have no license." >> $LOG_FILE
		return 1
	fi
	# if time expired, kill ceictims server
	while [ 1 ]; do
		if [ $TIME -le 0 ]; then
			echo "Stop $PRODUCT license. Reason: Time expired." >> $LOG_FILE
			import_into_timefile "license" "0"
			break
		else
			START_TIME=`date +%s`
			import_into_timefile "recorded_time" $START_TIME
			sleep 5
			if [[ `date +%s` -lt $START_TIME ]]; then
				continue
			else 
				if [[ `date +%s` -gt $(($START_TIME + 8)) ]]; then
					continue
				else
					TIME=$(($TIME + $START_TIME - `date +%s`))
					import_into_timefile "license" $TIME
				fi
			fi
		fi
	done

	return 1
}

check_and_start_license()
{
	CURRENT_TIME=`date +%s`
	
	if [ ! -f $TIME_FILE ]; then
		echo "Stop $PRODUCT license. Reason: $TIME_FILE file does not found." >> $LOG_FILE
		return 1
	else
		ERROR_TIMES=`awk '/error_times/{print $2}' $TIME_FILE`
		RECORDED_TIME=`awk '/recorded_time/{print $2}' $TIME_FILE`
		
		if [ "$RECORDED_TIME" != "" ]; then
			if [ $CURRENT_TIME -lt $RECORDED_TIME ]; then
				ERROR_TIMES=$(($ERROR_TIMES + 1))
				echo "Error times add" >> $LOG_FILE
				import_into_timefile "error_times" $ERROR_TIMES
				if [ $ERROR_TIMES -gt 3 ]; then
					echo "Stop $PRODUCT license, Reason: Error times greater then 3." >> $LOG_FILE
					return 1
				fi
			else
				STOP_TIME=$(($CURRENT_TIME - $RECORDED_TIME))
				LICENSE=`awk '/license/{print $2}' $TIME_FILE`
				import_into_timefile "license" $(($LICENSE - $STOP_TIME))
			fi
		fi

		start_license
		if [ $? == 1 ]; then
			return 1
		fi
	fi

	return 0
}

case $2 in
	start)
		hwclock --hctosys > /dev/null
		if [ "$PRODUCT" == "cmt" ]; then
			service ceictims start > /dev/null 2>&1
		fi
		check_and_start_license
		if [ $? == 1 -a $PRODUCT == "cmt" ]; then
			service ceictims stop > /dev/null 2>&1
			echo "Stop ceictims server" >> $LOG_FILE
		fi
	;;
	stop)
		PID=`ps aux | grep "/$SHELLNAME\ $1\ start" | awk '{print $2}'`
		if [ "$PID" == "" ]; then
			echo "Product $PRODUCT license does not in running."
		else
			kill -9 $PID
		fi
	;;
	*)
		echo "Usage: $SHELLNAME [product] {start|stop}"
		exit 1
	;;
esac



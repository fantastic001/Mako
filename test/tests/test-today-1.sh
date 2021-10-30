if [ -d ~/.mako ]; then 
	echo "backup of current mako database"
	mv ~/.mako mako.bak
fi

LOG_FILE="logs/today-1.log"
do_test() 
{
	set -x 
	echo "__________________________"
	mako projects add A
	mako projects add B
	mako project A subprojects add A1
	mako project B subprojects add B1
	mako project A subproject A1 tasks add mytask1 "$(date +%Y-%m)-28" 1
	mako project B subproject B1 tasks add mytask2 "$(date +%Y-%m)-28" 1
	mako schedule new 
	mako schedule add $(date +%w) 12 2 A A1
	mako schedule add $(date +%w) 15 1 B B1
	set +x
}

check_success() 
{
	(mako today | grep "mytask1") && \
		(mako today | grep "mytask2")
	return $?
}

log_error() 
{
	echo "TEST FAILED: today-1" >> $LOG_FILE
	
}

do_clean_success() 
{
	echo "$TESTCASE: Clean up"
	rm -rf ~/.mako/
	if [ -d mako.bak ]; then
		echo "restore real mako database"
		mv mako.bak ~/..mako
	fi
}

echo "Executing test today"
echo > $LOG_FILE

do_test
if ! check_success; then
	log_error

fi

do_clean_success

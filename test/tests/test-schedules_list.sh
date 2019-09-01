if [ -d ~/.mako ]; then 
	echo "backup of current mako database"
	mv ~/.mako mako.bak
fi

LOG_FILE="logs/schedules_list.log"
do_test() 
{
	set -x 
	echo "__________________________"
	mako projects add "test" 
	mako project "test" subprojects add subtest 
	mako project test subproject subtest tasks add mytask "$(date +%Y-%m)-28" 2
	mako schedule new
	mako schedule add 6 12 5 test subtest
	set +x
}

check_success() 
{
	mako schedules | grep "Schedule created $(date +%Y-%m-%d)"
	return $?
}

log_error() 
{
	echo "TEST FAILED: schedules_list" >> $LOG_FILE
	
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

echo "Executing test schedules_list"
echo > $LOG_FILE

do_test
if ! check_success; then
	log_error

fi

do_clean_success

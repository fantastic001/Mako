if [ -d ~/.mako ]; then 
	echo "backup of current mako database"
	mv ~/.mako mako.bak
fi

LOG_FILE="logs/schedule_remove.log"
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
	mako schedule remove 1 2 5
	mako schedule remove 6 12 1
	[ $(mako schedule | grep sub | wc -l) = 4 ]
	return $?
}

log_error() 
{
	echo "TEST FAILED: schedule_remove" >> $LOG_FILE
	
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

echo "Executing test schedule_remove"
echo > $LOG_FILE

do_test
if ! check_success; then
	log_error

fi

do_clean_success

if [ -d ~/.mako ]; then 
	echo "backup of current mako database"
	mv ~/.mako mako.bak
fi

LOG_FILE="logs/today.log"
do_test() 
{
	set -x 
	echo "__________________________"
	mako projects add "test" 
	mako project "test" subprojects add subtest 
	mako project test subproject subtest tasks add mytask "$(date +%Y-%m)-28" 2
	mako project test subproject subtest tasks add mytask "$(date +%Y-%m)-28" 2
	mako schedule new 
	mako schedule add $(date +%w) 12 12 test subtest
	set +x
}

check_success() 
{
	(mako today | grep "mytask") && ([ $(mako today | grep mytask | wc -l) = 2 ])
	return $?
}

log_error() 
{
	echo "TEST FAILED: today" >> $LOG_FILE
	
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

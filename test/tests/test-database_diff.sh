if [ -d ~/.mako ]; then 
	echo "backup of current mako database"
	mv ~/.mako mako.bak
fi

LOG_FILE="logs/database_diff.log"
do_test() 
{
	set -x 
	echo "__________________________"
	mako projects add "test" 
	mako project "test" subprojects add subtest 
	mako project test subproject subtest tasks add mytask "$(date +%Y-%m)-28" 2
	mako tables new testTable "a|b|c"
	set +x
}

check_success() 
{
	mako database diff 0
	(mako database diff 0 | grep "mytask" | grep "+") && \
		(mako database diff | grep "testTable")
	return $?
}

log_error() 
{
	echo "TEST FAILED: database_diff" >> $LOG_FILE
	
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

echo "Executing test database_diff"
echo > $LOG_FILE

do_test
if ! check_success; then
	log_error
fi

do_clean_success

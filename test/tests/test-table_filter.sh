if [ -d ~/.mako ]; then 
	echo "backup of current mako database"
	mv ~/.mako mako.bak
fi

LOG_FILE="logs/table_filter.log"
do_test() 
{
	set -x 
	echo "__________________________"
	mako projects add "test" 
	mako project "test" subprojects add subtest 
	mako project test subproject subtest tasks add mytask "$(date +%Y-%m)-28" 2
	mako tables new mytable "A|B|C"
	mako table mytable add "AAA|2|CCC"
	set +x
}

check_success() 
{
	mako table mytable filter CCC | grep AAA
	return $?
}

log_error() 
{
	echo "TEST FAILED: table_filter" >> $LOG_FILE
	
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

echo "Executing test table_filter"
echo > $LOG_FILE

do_test
if ! check_success; then
	log_error

fi

do_clean_success

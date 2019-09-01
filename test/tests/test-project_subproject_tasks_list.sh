if [ -d ~/.mako ]; then 
	echo "backup of current mako database"
	mv ~/.mako mako.bak
fi

LOG_FILE="logs/project_subproject_tasks_list.log"
do_test() 
{
	set -x 
	echo "__________________________"
	mako projects add "test" 
	mako project "test" subprojects add subtest 
	mako project test subproject subtest tasks add mytask "$(date +%Y-%m)-28" 2
	set +x
}

check_success() 
{
	mako project test subproject subtest tasks | grep mytask
	return $?
}

log_error() 
{
	echo "TEST FAILED: project_subproject_tasks_list" >> $LOG_FILE
	
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

echo "Executing test project_subproject_tasks_list"
echo > $LOG_FILE

do_test
if ! check_success; then
	log_error

fi

do_clean_success

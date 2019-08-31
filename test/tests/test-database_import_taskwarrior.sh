if [ -d ~/.mako ]; then 
	echo "backup of current mako database"
	mv ~/.mako mako.bak
fi

LOG_FILE="logs/database_import_taskwarrior.log"
do_test() 
{
	set -x 
	echo "__________________________"
	mako projects add "test" 
	mako project "test" subprojects add subtest 
	mako project test subproject subtest tasks add mytask "$(date +%Y-%m)-28" 2
	rm -rf ~/.mako/db/
	mako database import taskwarrior ~/.task/
	set +x
}

check_success() 
{
	[ -d ~/.mako/db ] 
	return $?
}

log_error() 
{
	echo "TEST FAILED: database_import_taskwarrior" >> $LOG_FILE
	
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

echo "Executing test database_import_taskwarrior"
echo > $LOG_FILE

do_test
if ! check_success; then
	log_error

fi

do_clean_success

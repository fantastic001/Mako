if [ -d ~/.mako ]; then 
	echo "backup of current mako database"
	mv ~/.mako mako.bak
fi

LOG_FILE="logs/reports_show.log"
do_test() 
{
	set -x 
	echo "__________________________"
	mako projects add "test" 
	mako project "test" subprojects add subtest 
	mako project test subproject subtest tasks add mytask "$(date +%Y-%m)-28" 2
	mako reports generate monthly 2018 1
	mako reports generate monthly 2018 2
	mako reports generate monthly 2018 3
	mako reports generate monthly 2018 4
	mako reports generate monthly 2018 5
	mako reports generate monthly 2019 12
	mako reports generate monthly "$(date +"%Y %m")"
	mako reports generate quarterly "$(date +"%Y")" 1
	mako reports generate quarterly "$(date +"%Y")" 2
	mako reports generate quarterly "$(date +"%Y")" 3
	mako reports generate quarterly "$(date +"%Y")" 4
	set +x
}

check_success() 
{
	mako reports show "Monthly report for $(date +%Y-%m-%d)" | grep "Expected time this month for each project"
	return $?
}

log_error() 
{
	echo "TEST FAILED: reports_show" >> $LOG_FILE
	
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

echo "Executing test reports_show"
echo > $LOG_FILE

do_test
if ! check_success; then
	log_error

fi

do_clean_success

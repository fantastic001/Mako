if [ -d ~/.mako ]; then 
	echo "backup of current mako database"
	mv ~/.mako mako.bak
fi

LOG_FILE="logs/metrics.log"
do_test() 
{
	set -x 
	echo "__________________________"
	mako projects add "test" 
	mako project "test" subprojects add subtest 
	mako project test subproject subtest tasks add mytask "$(date +%Y-%m)-28" 2
	mkdir ~/.mako/db/Measurements/opt/
	cat > ~/.mako/db/Measurements/opt/measure.json << EOF 
{
	"id": "measureOpt",
    "action": "filesystem.directory.size",
    "path": "/opt/",
    "description": "Measures size of opt"
} 
EOF
	set +x
}

check_success() 
{
	mako metrics | grep measureOpt
	return $?
}

log_error() 
{
	echo "TEST FAILED: metrics" >> $LOG_FILE
	
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

echo "Executing test metrics"
echo > $LOG_FILE

do_test
if ! check_success; then
	log_error

fi

do_clean_success

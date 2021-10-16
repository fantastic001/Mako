#!/bin/sh

mkdir -p logs

# backup old db 
rm -rf mako-old.bak
if [ -d ~/.mako ]; then 
	mv ~/.mako mako-old.bak
fi

for mytest in tests/*; do 
	rm -rf ~/.mako
	sh $mytest
done 

rm -rf ~/.mako

if [ -d mako-old.bak ]; then 
	mv mako-old.bak ~/.mako
fi

echo 
echo "Tests which failed:"
cat logs/* | grep "TEST FAILED"
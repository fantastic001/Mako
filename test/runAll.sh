#!/bin/sh


# first try to build docker image 
IMAGE_NAME="smoke_test_$$"
docker build -t $IMAGE_NAME:1.0 . 
if [ $? -ne 0 ]; then 
	echo "Couldn't build docker image"
	exit 1
fi
docker run -it --rm --name smoke_test_$$ $IMAGE_NAME:1.0 mako help 
if [ $? -ne 0 ]; then 
	echo "Couldn't run mako help"
	docker rmi $IMAGE_NAME:1.0
	exit 1
fi
docker rmi $IMAGE_NAME:1.0
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
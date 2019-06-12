#!/bin/sh

rm -rf mako
rm -rf src/*
cp -r ../src mako
echo "Generating apidoc ..."
sphinx-apidoc -o src mako
echo "Building html ..."
mako html

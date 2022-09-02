#!/bin/bash

cd lambda
zip -r lambda.zip . && mv lambda.zip ../../../deployment
cd ..


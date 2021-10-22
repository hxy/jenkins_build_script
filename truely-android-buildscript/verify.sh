#!/bin/bash
echo "Verify apk signature...."
SIGN_STRING=`$APKSIGNER_PATH/apksigner verify -v --print-certs $1|grep "v2 scheme"`
if echo $SIGN_STRING|grep -Fq false 
then 
	echo "v2 Signature is off." 
else 
	echo "Error. v2 Signature is on." 
	exit 1
fi
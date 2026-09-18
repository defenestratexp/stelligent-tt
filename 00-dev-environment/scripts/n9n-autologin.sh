#!/usr/bin/env bash

#################
### VARIABLES ###
#################
scriptName=$(basename "$0")
tempCredFile="/tmp/tempCreds.json"
getAccessKey='.Credentials.AccessKeyId'
getSecretKey='.Credentials.SecretAccessKey'
getSessionToken='.Credentials.SessionToken'
awsCredFile="$HOME/.aws/credentials"
# Long-lived profile used to request the session token
sourceProfile="${AWS_SOURCE_PROFILE:-n9n}"

#################
### FUNCTIONS ###
#################

# This is displayed is the script is called without a token
usage() {
    echo "MFA token required"
    echo "USAGE: $scriptName 123456"
    exit 1
}

# Find the MFA device ARN without hard-coding the account ID or user name.
# Order: $AWS_MFA_SERIAL, then mfa_serial in the profile's config, then IAM.
mfaSerial() {
    if [ -n "$AWS_MFA_SERIAL" ]; then
        echo "$AWS_MFA_SERIAL"
        return
    fi
    local serial
    serial=$(aws configure get mfa_serial --profile "$sourceProfile" 2>/dev/null)
    if [ -z "$serial" ]; then
        serial=$(aws iam list-mfa-devices --profile "$sourceProfile" \
            --query 'MFADevices[0].SerialNumber' --output text 2>/dev/null)
    fi
    if [ -z "$serial" ] || [ "$serial" = "None" ]; then
        echo "Could not determine the MFA device. Set AWS_MFA_SERIAL or add" >&2
        echo "mfa_serial to the '$sourceProfile' profile in ~/.aws/config." >&2
        exit 1
    fi
    echo "$serial"
}

# This gets a token from AWS and prepares the credentials file
login() {
    local token=$1
    local serial
    serial=$(mfaSerial) || exit 1

    # Obtain temporary creds from AWS
    aws sts get-session-token \
        --serial-number "$serial" \
        --token-code "$token" --profile "$sourceProfile" > "$tempCredFile"

    cleanConfig
    editConfig
}

# This deletes the temp json file and deletes the previous temp creds from the AWS cred file
cleanConfig() {
    # Edit the AWS cred file inline
    sed -i '1,/temp/!d' $awsCredFile
}

# This appends the new session login info to the AWS cred file
editConfig() {
    accessKey=$(jq -r $getAccessKey $tempCredFile)
    secretAccessKey=$(jq -r $getSecretKey $tempCredFile)
    sessionToken=$(jq -r $getSessionToken $tempCredFile)

    echo "output = json" >> $awsCredFile
    echo "region = us-west-2" >> $awsCredFile
    echo "aws_access_key_id = $accessKey" >> $awsCredFile
    echo "aws_secret_access_key = $secretAccessKey" >> $awsCredFile
    echo "aws_session_token = $sessionToken" >> $awsCredFile

    rm -rf $tempCredFile
}

############
### MAIN ###
############

# Easier to parse JSON with jq. Make sure it is installed
jqPath=$(which jq)
if [ -z "$jqPath" ]; then
    echo "This script requires jq. Just a second"
    sudo apt -y install jq
fi

# Error out if no MFA token is given
if [ -z "$1" ]; then
    usage
else
    token=$1
    login $token
fi
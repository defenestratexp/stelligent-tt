#!/usr/bin/env bash
#
# n9n-autologin.sh - trade a long-lived IAM user key plus an MFA code for
# temporary STS session credentials, and store them in a named profile.
#
# This is the worked example for Lab 0.1.4 (the MFA + STS exercise). The 2026
# edition's day-to-day path is IAM Identity Center (`aws configure sso`), which
# needs no script at all.
#
# USAGE: n9n-autologin.sh 123456
#
# Environment (all optional):
#   AWS_SOURCE_PROFILE    profile holding the long-lived key (default: n9n)
#   AWS_TARGET_PROFILE    profile that receives the session creds (default: temp)
#   AWS_MFA_SERIAL        MFA device ARN; otherwise read from the source profile's
#                         mfa_serial in ~/.aws/config, otherwise looked up in IAM
#   AWS_SESSION_DURATION  session length in seconds (default: 43200 = 12 hours)

set -euo pipefail

#################
### VARIABLES ###
#################
scriptName=$(basename "$0")
# Long-lived profile used to request the session token
sourceProfile="${AWS_SOURCE_PROFILE:-n9n}"
# Profile the temporary credentials are written to
targetProfile="${AWS_TARGET_PROFILE:-temp}"
sessionDuration="${AWS_SESSION_DURATION:-43200}"
# Course lab region, used only if the source profile has no region of its own
defaultRegion="us-east-2"
tempCredFile=""

#################
### FUNCTIONS ###
#################

# Displayed if the script is called without a valid token
usage() {
    echo "MFA token required" >&2
    echo "USAGE: $scriptName 123456" >&2
    exit 1
}

# Remove the temporary JSON file however the script exits
cleanup() {
    if [ -n "$tempCredFile" ] && [ -f "$tempCredFile" ]; then
        rm -f "$tempCredFile"
    fi
}

# Find the MFA device ARN without hard-coding the account ID or user name.
# Order: $AWS_MFA_SERIAL, then mfa_serial in the profile's config, then IAM.
mfaSerial() {
    if [ -n "${AWS_MFA_SERIAL:-}" ]; then
        echo "$AWS_MFA_SERIAL"
        return
    fi
    local serial
    serial=$(aws configure get mfa_serial --profile "$sourceProfile" 2>/dev/null || true)
    if [ -z "$serial" ]; then
        serial=$(aws iam list-mfa-devices --profile "$sourceProfile" \
            --query 'MFADevices[0].SerialNumber' --output text 2>/dev/null || true)
    fi
    if [ -z "$serial" ] || [ "$serial" = "None" ]; then
        echo "Could not determine the MFA device. Set AWS_MFA_SERIAL or add" >&2
        echo "mfa_serial to the '$sourceProfile' profile in ~/.aws/config." >&2
        exit 1
    fi
    echo "$serial"
}

# Region for the target profile: the source profile's region, else the lab default
targetRegion() {
    local region
    region=$(aws configure get region --profile "$sourceProfile" 2>/dev/null || true)
    echo "${region:-$defaultRegion}"
}

# Get a session token from STS. Nothing in ~/.aws is touched unless this succeeds.
login() {
    local token=$1
    local serial
    serial=$(mfaSerial)

    # Private temp file: mode 600 regardless of the caller's umask, removed on exit
    tempCredFile=$(mktemp "${TMPDIR:-/tmp}/${scriptName%.sh}.XXXXXX")
    chmod 600 "$tempCredFile"

    if ! aws sts get-session-token \
        --serial-number "$serial" \
        --token-code "$token" \
        --duration-seconds "$sessionDuration" \
        --profile "$sourceProfile" \
        --output json > "$tempCredFile"; then
        echo "get-session-token failed; profile '$targetProfile' left unchanged." >&2
        exit 1
    fi

    writeProfile
}

# Update only the target profile. `aws configure set` puts the keys in
# ~/.aws/credentials and region/output in ~/.aws/config, and leaves every
# other profile alone.
# Note: the values are passed as arguments, so they are briefly visible to
# other users of this machine in the process list. Acceptable on a
# single-user laptop; another reason to prefer IAM Identity Center.
writeProfile() {
    local accessKey secretAccessKey sessionToken expiration region
    accessKey=$(jq -r '.Credentials.AccessKeyId' "$tempCredFile")
    secretAccessKey=$(jq -r '.Credentials.SecretAccessKey' "$tempCredFile")
    sessionToken=$(jq -r '.Credentials.SessionToken' "$tempCredFile")
    expiration=$(jq -r '.Credentials.Expiration' "$tempCredFile")

    for value in "$accessKey" "$secretAccessKey" "$sessionToken"; do
        if [ -z "$value" ] || [ "$value" = "null" ]; then
            echo "Unexpected response from STS; profile '$targetProfile' left unchanged." >&2
            exit 1
        fi
    done

    region=$(targetRegion)

    aws configure set aws_access_key_id "$accessKey" --profile "$targetProfile"
    aws configure set aws_secret_access_key "$secretAccessKey" --profile "$targetProfile"
    aws configure set aws_session_token "$sessionToken" --profile "$targetProfile"
    aws configure set region "$region" --profile "$targetProfile"
    aws configure set output json --profile "$targetProfile"

    echo "Profile '$targetProfile' updated (region $region), expires $expiration."
    echo "Use it with: export AWS_PROFILE=$targetProfile"
}

############
### MAIN ###
############

trap cleanup EXIT

# Error out if no MFA token is given, or it isn't a 6-digit code
if [ $# -ne 1 ] || ! [[ $1 =~ ^[0-9]{6}$ ]]; then
    usage
fi

# Both tools are required; say so rather than installing anything
for tool in aws jq; do
    if ! command -v "$tool" > /dev/null 2>&1; then
        echo "This script requires '$tool'. Install it and run again." >&2
        exit 1
    fi
done

login "$1"

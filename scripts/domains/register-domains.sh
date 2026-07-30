#!/usr/bin/env bash
# JHI-SIG: 69M2705M | Register the aegiraenterprise.* domain family via Route 53 | JHI Research & Analytics Firm, Inc. (proprietary)
#
# Registers aegiraenterprise .ai / .io / .dev / .app through Amazon Route 53 Domains.
# Run this from a shell authenticated to the AWS account that owns aegiraenterprise.com
# (aws configure / SSO / an IAM role with route53domains:RegisterDomain).
#
# Contact/registrant PII is read from a LOCAL, gitignored file (default: contact.json in
# this directory) — copy contact.example.json -> contact.json and fill it in. Nothing with
# PII is committed. Registration is a PAID action; review the prices in
# docs/DOMAIN_REGISTRATION_RUNBOOK.md before running.
#
# Usage:
#   scripts/domains/register-domains.sh [path/to/contact.json]
#
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
CONTACT="${1:-$DIR/contact.json}"
REGION="us-east-1"          # route53domains APIs must run in us-east-1

command -v aws >/dev/null 2>&1 || { echo "ERROR: aws CLI not found. Install it and run 'aws configure'."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 not found (used to assemble the request JSON)."; exit 1; }
[ -f "$CONTACT" ] || { echo "ERROR: contact file not found: $CONTACT"; echo "Copy $DIR/contact.example.json -> $DIR/contact.json and fill it in."; exit 1; }

echo "AWS identity:"; aws sts get-caller-identity --output text || { echo "ERROR: not authenticated to AWS."; exit 1; }

# domain : DurationInYears : PrivacyProtect
#   .ai (Anguilla ccTLD) has a 2-YEAR minimum; if it rejects WHOIS privacy, set its flag to false.
DOMAINS=(
  "aegiraenterprise.ai:2:true"
  "aegiraenterprise.io:1:true"
  "aegiraenterprise.dev:1:true"
  "aegiraenterprise.app:1:true"
)

for entry in "${DOMAINS[@]}"; do
  IFS=":" read -r name years privacy <<<"$entry"
  payload="$DIR/${name}.register.json"
  python3 - "$CONTACT" "$name" "$years" "$privacy" >"$payload" <<'PY'
import json, sys
contact = json.load(open(sys.argv[1]))
name, years, privacy = sys.argv[2], int(sys.argv[3]), sys.argv[4].lower() == "true"
doc = {
    "DomainName": name,
    "DurationInYears": years,
    "AutoRenew": True,
    "AdminContact": contact,
    "RegistrantContact": contact,
    "TechContact": contact,
    "PrivacyProtectAdminContact": privacy,
    "PrivacyProtectRegistrantContact": privacy,
    "PrivacyProtectTechContact": privacy,
}
print(json.dumps(doc, indent=2))
PY

  echo "==> Registering ${name} (${years} yr, privacy=${privacy})"
  op=$(aws route53domains register-domain \
        --region "$REGION" \
        --cli-input-json "file://${payload}" \
        --query OperationId --output text)
  echo "    OperationId: ${op}"
  printf "%s\t%s\t%s\n" "$(date -u +%FT%TZ)" "$name" "$op" >>"$DIR/operations.log"
done

echo
echo "All registration requests submitted. Track each with:"
echo "  aws route53domains get-operation-detail --region ${REGION} --operation-id <OperationId>"
echo "OperationIds saved to ${DIR}/operations.log"

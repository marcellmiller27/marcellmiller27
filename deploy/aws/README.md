<!-- JHI-SIG: 69M2705M | Build & Deploy | JHI Research & Analytics Firm, Inc. (proprietary) -->
# Aegira — AWS one-time infrastructure (CloudFormation)

These templates provision the always-on AWS-native footprint for **Aegira**
(product) / **JHI Research & Analytics Firm, Inc.** (publisher). They pair with
the board-ready construct in [`docs/AWS_DEPLOYMENT_CONSTRUCT.md`](../../docs/AWS_DEPLOYMENT_CONSTRUCT.md)
and the CI pipeline in [`.github/workflows/deploy.yml`](../../.github/workflows/deploy.yml).

> **No real secrets, account IDs, or credentials are in these files.** Every
> account-specific value is a clearly-labeled parameter/placeholder
> (`REPLACE_WITH_...`, `ACCOUNT_ID`, `REGION`). Runtime secret *values* are never
> committed — `03-secrets.yaml` creates empty secrets you populate out-of-band.

Region: **us-east-1** (same as Bedrock/SES).

## Stacks & deploy order

| # | Template | Scope | Depends on |
|---|----------|-------|------------|
| 1 | `01-ecr.yaml` | Private ECR repos (backend + frontend) | — (account-wide, once) |
| 2 | `02-github-oidc-deploy-role.yaml` | GitHub OIDC provider + least-privilege CI role | 01 (repo ARNs) |
| 3 | `03-secrets.yaml` | Secrets Manager scaffolding (keys only) | — (per env) |
| 4 | `04-network.yaml` | VPC, subnets, NAT, RDS SG, connector SG | — (per env) |
| 5 | `05-rds-postgres.yaml` | Private RDS PostgreSQL | 04 |
| 6 | `06-apprunner-services.yaml` | App Runner backend + frontend + VPC connector | 01, 03, 04, 05 |

Stacks 3–6 are **per environment** (`EnvironmentName=staging`, then
`production`). Stacks 1–2 are account-wide (deploy once).

## Example: bring up staging

```bash
export AWS_REGION=us-east-1
ENV=staging

# 1) Account-wide: ECR + OIDC deploy role (deploy once total).
aws cloudformation deploy --template-file 01-ecr.yaml \
  --stack-name aegira-ecr --capabilities CAPABILITY_NAMED_IAM

aws cloudformation deploy --template-file 02-github-oidc-deploy-role.yaml \
  --stack-name aegira-oidc --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides GitHubOrg=YOUR_ORG GitHubRepo=YOUR_REPO \
    BackendRepositoryArn=<from 01 output> FrontendRepositoryArn=<from 01 output>

# 2) Per environment: secrets -> network -> rds -> app runner.
aws cloudformation deploy --template-file 03-secrets.yaml \
  --stack-name aegira-$ENV-secrets --parameter-overrides EnvironmentName=$ENV

aws cloudformation deploy --template-file 04-network.yaml \
  --stack-name aegira-$ENV-network --parameter-overrides EnvironmentName=$ENV

aws cloudformation deploy --template-file 05-rds-postgres.yaml \
  --stack-name aegira-$ENV-rds --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides EnvironmentName=$ENV

# 3) Populate the secret VALUES (out-of-band, never committed). At minimum:
#    - compose DATABASE_URL from the RDS endpoint + the RDS-managed master
#      secret and put it in aegira/$ENV/DATABASE_URL
#    - openssl rand -hex 32  ->  aegira/$ENV/AUTH_JWT_SECRET
aws secretsmanager put-secret-value --secret-id aegira/$ENV/AUTH_JWT_SECRET \
  --secret-string "$(openssl rand -hex 32)"

# 4) App Runner (needs the first images already pushed to ECR — let the pipeline
#    push once, or push a bootstrap image manually).
aws cloudformation deploy --template-file 06-apprunner-services.yaml \
  --stack-name aegira-$ENV-apprunner --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides EnvironmentName=$ENV \
    BackendImageUri=<ecr-uri>/aegira/backend:$ENV \
    FrontendImageUri=<ecr-uri>/aegira/frontend:$ENV
```

## The frontend↔backend wiring gotcha

App Runner gives the two services **separate, stable URLs**. Next.js bakes its
`/api/v1` proxy target at **build time**, so the frontend image must be built
with `API_PROXY_TARGET=<backend service URL>`. Two supported patterns (see the
construct doc for detail):

1. **Two-phase (pipeline default):** create/deploy the backend first, read its
   URL via `aws apprunner describe-service`, then build the frontend image with
   that URL as the build arg.
2. **Stable custom domain:** assign `api.aegiraenterprise.com` to the backend
   service and always build the frontend with `API_PROXY_TARGET=https://api.aegiraenterprise.com`.

## GitHub secrets/vars the pipeline needs

See the table in [`docs/AWS_DEPLOYMENT_CONSTRUCT.md`](../../docs/AWS_DEPLOYMENT_CONSTRUCT.md#github-secrets--vars).

## Validation (no AWS access required)

```bash
# Plain-YAML parse (these templates use long-form intrinsics on purpose):
python -c "import yaml,glob; [yaml.safe_load(open(f)) for f in glob.glob('deploy/aws/*.y*ml')]"
# If installed, deeper checks:
cfn-lint deploy/aws/*.yaml
```

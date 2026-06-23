# John Henry Investments Cloud Storage and Capacity Plan

## Purpose

This document estimates cloud storage, database capacity, network throughput, and processing-speed requirements for the John Henry Investments platform as the user network grows.

These are planning estimates for infrastructure sizing. Actual production requirements should be validated with real usage analytics, load testing, provider monitoring, and cost reports.

## Platform workloads considered

The estimates cover:

- User accounts and organizations
- Portfolio dashboards
- Accounting journal entries
- Audit logs
- CRM contacts, deals, and activities
- External banking and vendor sync records
- AI assistant conversations
- Opportunity scoring records
- Uploaded due diligence documents
- Generated Excel, Word, CSV, and PDF reports
- Database backups
- API traffic
- Background processing jobs

## User growth tiers

| Tier | Users | Organizations | Description |
| --- | ---: | ---: | --- |
| Prototype | 100 | 25 | Internal testing, demos, early reviewers |
| MVP launch | 1,000 | 250 | First paid customers and small teams |
| Growth | 10,000 | 2,500 | Meaningful B2C/B2B adoption |
| Scale | 50,000 | 10,000 | Large consumer/professional network |
| Enterprise scale | 100,000 | 20,000+ | National platform with enterprise teams |

## Storage assumptions

Average monthly storage per active user:

| Data type | Estimated monthly data per active user | Notes |
| --- | ---: | --- |
| Profile, account, subscription records | 25 KB | Small structured records |
| Dashboard, portfolio, watchlist records | 250 KB | Holdings, metrics, preferences |
| Accounting, CRM, integration records | 500 KB | Journal entries, contacts, deals, sync logs |
| AI chat and opportunity score history | 2 MB | Prompts, responses, scores, metadata |
| Generated reports | 10 MB | PDF, Excel, Word, CSV outputs |
| Uploaded due diligence documents | 50 MB | Tax returns, P&L, balance sheets, bank statements |
| Audit logs and event records | 250 KB | Security, billing, integration, data changes |

Estimated monthly net-new storage:

```text
~63 MB per active user per month
```

Recommended planning buffer:

```text
100 MB per active user per month
```

This buffer accounts for larger documents, duplicate uploads, generated exports, indexes, metadata, and retained versions.

## Estimated object/file storage requirements

Object storage includes uploaded documents, generated reports, exports, and evidence files.

| Tier | Monthly object storage growth | 12-month storage | 36-month storage |
| --- | ---: | ---: | ---: |
| Prototype - 100 users | 10 GB/month | 120 GB | 360 GB |
| MVP - 1,000 users | 100 GB/month | 1.2 TB | 3.6 TB |
| Growth - 10,000 users | 1 TB/month | 12 TB | 36 TB |
| Scale - 50,000 users | 5 TB/month | 60 TB | 180 TB |
| Enterprise - 100,000 users | 10 TB/month | 120 TB | 360 TB |

Recommended services:

- AWS S3
- Supabase Storage for early-stage usage
- Azure Blob Storage if Microsoft enterprise integration is prioritized

Storage class recommendation:

- Hot storage for recent 90 days
- Infrequent access storage after 90-180 days
- Archive storage after policy-defined retention period

## Estimated relational database size

Database storage includes users, organizations, memberships, subscriptions, accounting records, CRM records, integration metadata, audit logs, reports metadata, opportunity scores, and AI metadata.

| Tier | Starting DB size | 12-month DB size | 36-month DB size |
| --- | ---: | ---: | ---: |
| Prototype - 100 users | 1-5 GB | 5-10 GB | 10-25 GB |
| MVP - 1,000 users | 10-25 GB | 50-100 GB | 150-300 GB |
| Growth - 10,000 users | 100-250 GB | 500 GB-1 TB | 1.5-3 TB |
| Scale - 50,000 users | 500 GB-1 TB | 2.5-5 TB | 7.5-15 TB |
| Enterprise - 100,000 users | 1-2 TB | 5-10 TB | 15-30 TB |

Recommended database path:

| Tier | Recommended database |
| --- | --- |
| Prototype | SQLite for local development only |
| MVP | Supabase PostgreSQL or managed PostgreSQL |
| Growth | Dedicated PostgreSQL with read replicas |
| Scale | Partitioned PostgreSQL, read replicas, separate analytics warehouse |
| Enterprise | PostgreSQL plus data warehouse and object-storage data lake |

Database design requirements:

- Index organization ID on all tenant-owned tables
- Use composite indexes for report, date, and status filters
- Partition high-volume audit logs and sync logs by date
- Separate transactional database from analytics warehouse at scale
- Add connection pooling
- Add read replicas once dashboard/report reads grow

## Backup and retention estimates

Recommended backup policy:

| Data type | Retention |
| --- | --- |
| Database point-in-time recovery | 7-35 days |
| Daily database snapshots | 35-90 days |
| Monthly database snapshots | 12-84 months depending on compliance |
| Uploaded documents | Policy-defined, often 3-7 years for financial records |
| Audit logs | 7 years for regulated financial workflows if legally required |
| Generated reports | 3-7 years depending on customer and compliance needs |

Storage multiplier for backups:

```text
2x to 4x primary database storage
```

Example:

```text
1 TB production database may require 2-4 TB total backup and retention storage.
```

## API traffic and network throughput estimates

Assumptions:

- Average active user performs 50-150 API requests per day.
- Professional and enterprise users perform heavier report, CRM, upload, and integration workloads.
- Peak traffic is 5x to 10x average traffic.

Estimated API volume:

| Tier | Daily API requests | Peak requests per second |
| --- | ---: | ---: |
| Prototype - 100 users | 5,000-15,000 | 5-20 RPS |
| MVP - 1,000 users | 50,000-150,000 | 25-100 RPS |
| Growth - 10,000 users | 500,000-1.5M | 200-750 RPS |
| Scale - 50,000 users | 2.5M-7.5M | 1,000-3,000 RPS |
| Enterprise - 100,000 users | 5M-15M | 2,000-6,000 RPS |

Recommended network services:

- CDN for front-end assets
- API gateway or load balancer
- WAF for public traffic
- Rate limiting for AI, reports, and upload endpoints
- Private networking between API, database, cache, and workers

## File upload throughput estimates

Assumptions:

- Average due diligence document: 2-10 MB
- Large bank statement or report package: 20-100 MB
- Upload spikes occur during acquisition diligence and report preparation

Recommended limits:

| Tier | Max file size | Daily upload volume | Recommended upload path |
| --- | ---: | ---: | --- |
| Prototype | 25 MB | <10 GB/day | Direct API upload acceptable |
| MVP | 50 MB | 10-100 GB/day | Signed object-storage uploads |
| Growth | 100 MB | 100 GB-1 TB/day | Signed uploads with async processing |
| Scale | 250 MB | 1-5 TB/day | Multipart upload and background scanning |
| Enterprise | 500 MB+ | 5-10 TB/day | Multipart upload, virus scanning, DLP review |

Recommendation:

```text
Use signed direct-to-object-storage upload URLs instead of routing large files through the API server.
```

## Processing-speed requirements

Processing workloads:

- API request handling
- Authentication/session validation
- Dashboard aggregation
- Report generation
- AI assistant requests
- Banking/vendor sync jobs
- Document extraction
- PDF, Excel, and Word exports
- Audit-log writes

Recommended latency targets:

| Operation | Target response time |
| --- | ---: |
| Login/session validation | <300 ms |
| Dashboard API response | <500 ms |
| CRUD operations | <300 ms |
| Search/filter operations | <1 second |
| Report metadata request | <1 second |
| Generated PDF/Excel/Word report | Async job, 5 seconds-5 minutes |
| AI assistant response | Streaming preferred, first token <2 seconds |
| Document extraction | Async job, 1-15 minutes depending on size |
| Banking/vendor sync | Async job, 1-30 minutes depending on provider |

## Compute sizing estimates

Backend API compute:

| Tier | API compute recommendation |
| --- | --- |
| Prototype | 1 small API instance, 1-2 vCPU, 1-2 GB RAM |
| MVP | 2 API instances, 2 vCPU, 4 GB RAM each |
| Growth | 4-8 API instances, 2-4 vCPU, 4-8 GB RAM each |
| Scale | Autoscaling API pool, 8-20 instances, 4-8 vCPU each |
| Enterprise | Multi-region autoscaling, separate read/write and worker services |

Background worker compute:

| Tier | Worker recommendation |
| --- | --- |
| Prototype | Same host or 1 small worker |
| MVP | 1-2 workers for reports and integrations |
| Growth | Dedicated worker pool for reports, documents, AI, and sync jobs |
| Scale | Separate worker queues by workload |
| Enterprise | Multi-queue, autoscaled workers with priority tiers |

Recommended queues:

- `reports`
- `documents`
- `ai`
- `integrations`
- `billing`
- `audit`

## Cache and performance requirements

Recommended cache:

- Redis or managed equivalent

Cache uses:

- Session metadata
- Plan entitlement lookups
- Dashboard aggregates
- Market data snapshots
- Rate-limit counters
- Report job status
- AI conversation streaming state

Suggested cache sizes:

| Tier | Cache memory |
| --- | ---: |
| Prototype | 256 MB-1 GB |
| MVP | 1-4 GB |
| Growth | 8-16 GB |
| Scale | 32-64 GB |
| Enterprise | Clustered Redis / managed cache |

## AI processing estimates

AI workloads can become the largest variable cost and latency driver.

Assumptions:

- Consumer user: 10-30 AI requests/month
- Professional user: 50-200 AI requests/month
- Enterprise user: 500-5,000 AI requests/month per organization

Recommended controls:

- Rate limits by plan
- Monthly AI usage quotas
- Token budgeting
- Prompt and response caching
- User confirmation before expensive research jobs
- Async processing for large document analysis
- Redaction before AI provider calls

Plan-based AI quota example:

| Plan | Monthly AI requests | Max document analysis jobs |
| --- | ---: | ---: |
| Consumer | 50 | 5 |
| Professional | 500 | 50 |
| Enterprise | Custom | Custom |

## Database performance requirements

Recommended performance targets:

| Metric | MVP target | Growth target | Scale target |
| --- | ---: | ---: | ---: |
| Simple lookup query | <50 ms | <50 ms | <50 ms |
| Dashboard aggregate query | <300 ms | <500 ms | <750 ms |
| Report metadata query | <500 ms | <750 ms | <1 second |
| Audit log write | <100 ms | <150 ms | <250 ms |
| Connection pool | 10-25 | 50-100 | 100-300 |

Recommended indexes:

- `organization_id`
- `user_id`
- `created_at`
- `status`
- `plan`
- `report_type`
- `external_provider`
- `sync_job_id`
- `entry_date`
- `account_code`

## Observability requirements

Track:

- API response time
- API error rate
- Database query latency
- Database storage growth
- Object storage growth
- Upload failure rate
- Report job duration
- AI request latency and token usage
- Integration sync success/failure rate
- Billing webhook success/failure rate
- Queue depth
- Worker job retries
- Login failure rate

Recommended alert thresholds:

| Metric | Alert threshold |
| --- | --- |
| API error rate | >2% for 5 minutes |
| API p95 latency | >1 second for 10 minutes |
| Database CPU | >80% for 15 minutes |
| Database storage | >80% allocated |
| Queue depth | >1,000 pending jobs or growing for 15 minutes |
| Failed billing webhooks | Any sustained failure |
| Failed integration syncs | >5% failure rate |
| Object storage growth | >25% above forecast |

## Recommended architecture by stage

### Prototype

- Vercel or local Next.js
- FastAPI on a small instance
- SQLite for development only
- Local/test object storage
- No production user data

### MVP

- Vercel for front end
- FastAPI on managed container or app service
- Supabase PostgreSQL or managed PostgreSQL
- Supabase Storage or S3
- Redis cache
- Background worker
- Stripe billing
- Basic monitoring

### Growth

- CDN and WAF
- API autoscaling
- PostgreSQL read replica
- Dedicated worker queues
- Object-storage lifecycle policies
- Central logging and error tracking
- Analytics warehouse for heavy reporting

### Scale / Enterprise

- Multi-region front-end delivery
- Multi-zone backend deployment
- PostgreSQL partitioning and replicas
- Separate transactional and analytics systems
- Dedicated AI/document processing workers
- Enterprise key management
- Advanced compliance logging
- Data retention automation

## Recommended starting capacity for paid MVP

For a realistic paid MVP supporting up to 1,000 users:

```text
Database: 100 GB managed PostgreSQL
Object storage: 1-2 TB
API compute: 2 instances, 2 vCPU / 4 GB RAM each
Workers: 1-2 worker instances, 2 vCPU / 4 GB RAM each
Cache: 1-4 GB Redis
Bandwidth: 1-5 TB/month
Backup storage: 300-500 GB for database backups
Monitoring: API, DB, storage, queue, billing, and integration alerts
```

## Recommended starting capacity for 10,000 users

```text
Database: 500 GB-1 TB managed PostgreSQL
Object storage: 12-24 TB
API compute: 4-8 instances, 2-4 vCPU / 4-8 GB RAM each
Workers: 4-12 workers separated by queue type
Cache: 8-16 GB Redis
Bandwidth: 10-25 TB/month
Backup storage: 2-4 TB
Analytics: Separate warehouse or read replica
```

## Recommended starting capacity for 100,000 users

```text
Database: 5-10 TB transactional storage plus analytics warehouse
Object storage: 120 TB/year growth planning
API compute: Autoscaling, multi-zone, 20+ service instances as needed
Workers: Separate autoscaled pools for AI, reports, documents, integrations, billing
Cache: 64 GB+ clustered Redis or managed cache
Bandwidth: 100 TB+/month depending on document/report usage
Backup storage: 20-40 TB depending on retention
Analytics: Dedicated warehouse and data lake
```

## Key capacity risks

- Due diligence document uploads can grow object storage quickly.
- AI assistant and document analysis can create high variable costs.
- Audit logs and integration sync logs can become high-volume tables.
- Generated reports can duplicate data already stored elsewhere.
- Enterprise teams can create concentrated spikes in document uploads and report jobs.
- Banking/vendor integrations require retries and provider-specific rate-limit handling.

## Recommended next infrastructure action items

- [ ] Choose production database provider.
- [ ] Choose object storage provider.
- [ ] Define file retention policy.
- [ ] Define audit-log retention policy.
- [ ] Define AI usage quotas by plan.
- [ ] Define report generation limits by plan.
- [ ] Add database migrations.
- [ ] Add storage lifecycle policy.
- [ ] Add background job queue.
- [ ] Add Redis or managed cache.
- [ ] Add monitoring and alerting.
- [ ] Run load test for 1,000-user MVP profile.
- [ ] Run storage-cost forecast for 1,000, 10,000, 50,000, and 100,000 users.

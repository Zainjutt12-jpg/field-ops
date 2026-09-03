# FieldOps API

Learning / portfolio skeleton of a **multi-portal Django + DRF backend**.

Same architectural shape as a production audience-partitioned service (admin cpanel, client portal, field mobile, wallet, public integration API) — rebuilt as a small **field-service / work-order** domain for GitHub review.

This repo is **structure + real API layout only** (views, serializers, urls, logics). No seeded DB or runtime demo setup required to understand the design.

## Architecture highlights

- Domain apps split by concern (`accounts`, `catalog`, `operations`, portals, `wallet`, `public_api`)
- Audience URL mounts: `/cpanel/`, `/client/`, `/field/`, `/wallet/`, `/api/`
- Versioned packages: `api/v1/{Views,Serializers}`
- Thin `APIView`s → serializers → `CommonLogics` / `services`
- JWT role permissions + partner `api_token` header auth
- Shared `BaseModel` / soft-delete, pagination, exception envelope
- Split settings: `config/settings/{base,local,production}.py`

## Layout

```
fieldops-api/
├── config/                 # project package + settings
├── common/                 # BaseModel, pagination, permissions, health
├── accounts/               # custom User, login history
├── catalog/                # regions, statuses, service types
├── operations/             # Client + WorkOrder + CommonLogics
├── admin_portal/           # /cpanel  APIs
├── client_portal/          # /client  APIs
├── field/                  # /field   APIs
├── wallet/                 # /wallet  maker-checker payouts
├── public_api/             # /api     partner token APIs
├── jobs/                   # management commands (placeholder)
└── utils/                  # shared helpers
```

## API map (structure)

| Mount | Role |
|-------|------|
| `POST /cpanel/api/v1/auth/login/` | Admin JWT login |
| `GET/POST /cpanel/api/v1/clients/` | Clients (admin) |
| `GET /cpanel/api/v1/work-orders/` | Work orders (admin) |
| `POST /cpanel/api/v1/work-orders/{ref}/assign/` | Assign technician |
| `POST /client/api/v1/auth/login/` | Client JWT login |
| `GET/POST /client/api/v1/work-orders/` | Client work orders |
| `POST /field/api/v1/auth/login/` | Field JWT login |
| `GET /field/api/v1/work-orders/mine/` | Assigned jobs |
| `POST /field/api/v1/work-orders/{ref}/complete/` | Complete job |
| `GET/POST /wallet/api/v1/payouts/` | Payout drafts |
| `POST /wallet/api/v1/payouts/{id}/submit/` | Submit approval |
| `POST /wallet/api/v1/payouts/{id}/approve/` | Approve |
| `POST /api/v1/work-orders/` | Public create (`api_token` header) |
| `GET /health/` | Health check |

## Stack

Django 5.1 · DRF 3.15 · SimpleJWT · django-environ · cors-headers

## Note

Skeleton for learning / showcasing patterns — not a production-ready product.

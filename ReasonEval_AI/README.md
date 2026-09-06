# ReasonEval AI — V8 Production Beta

ReasonEval AI is a math-first reasoning-evaluation and assessment platform for students, faculty and institutions.

## Current V8 capabilities
- hybrid deterministic + reasoning evaluation,
- student public assignment links and tracking receipts,
- institution roles: owner / admin / faculty / reviewer,
- department → course → assignment workflow,
- CSV/XLSX import,
- faculty/reviewer override with audit trail,
- PDF feedback reports and CSV exports,
- PostgreSQL-ready SQLAlchemy data layer,
- SMTP invitation support,
- Razorpay-ready server order / signature / webhook flow,
- Docker and Railway deployment configuration.

## Railway deployment
This project is stored as a subdirectory of the existing portfolio repository.

In Railway:
1. Deploy from GitHub.
2. Select `ajaynitw1995/my`.
3. Set **Root Directory** to `/reasoneval-ai`.
4. Add a PostgreSQL service.
5. Set the web service `DATABASE_URL` from the Postgres service reference.
6. Generate a Railway domain.
7. Set `APP_BASE_URL` and `ALLOWED_ORIGINS` to that domain.

The Docker wrapper extracts the tested V8 source bundle at build time. The complete readable source package is also available as the bundled ZIP.

## Pilot rule
During the first faculty pilot, every automated score should remain subject to faculty review. ReasonEval explicitly stores system confidence, review-required flags and human overrides instead of presenting AI judgment as ground truth.

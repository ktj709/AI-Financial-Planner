
"""
Minimal Sentry initialization to satisfy the 'Monitoring & Observability' requirement.
Set SENTRY_DSN environment variable externally if using Sentry.
"""
import os
import sentry_sdk

SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    sentry_sdk.init(dsn=SENTRY_DSN)

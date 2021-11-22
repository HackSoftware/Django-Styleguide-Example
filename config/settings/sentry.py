from config.env import env

SENTRY_DSN = env('SENTRY_DSN', default='')

if SENTRY_DSN:
    environment = env("SENTRY_ENVIRONMENT", default="local")
    # This is related to Sentry's performance monitoring
    # https://docs.sentry.io/product/performance/
    # If you don't need it, just remove everything related to `track_performance`
    track_performance = environment == "production"

    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.celery import CeleryIntegration

    # We are implementing this following the official documentation:
    # https://docs.sentry.io/platforms/python/performance/
    # This specific implementation ignores the execute times of all Celery tasks.
    # But if you want to also traces them, just change the return value for the Celery tasks.
    def traces_sampler(sampling_context):
        """
        We want to track only web transactions, and ignore all Celery transactions.
        Here's an example context from Celery:
        {
            "transaction_context": {
                "trace_id": "08c7c8b4d8744977a24d40457fc36d0b",
                "span_id": "9a78f06a999ae7a2",
                "parent_span_id": "808dca474783eb78",
                "same_process_as_parent": false,
                "op": "celery.task",
                "description": null,
                "start_timestamp": "datetime here",
                "timestamp": null,
                "tags": {
                    "status": "ok"
                },
                "name": "project.app.tasks.task_name",
                "sampled": null
            },
            "parent_sampled": true,
            "celery_job": {
                "task": "project.app.tasks.task_name",
                "args": [],
                "kwargs": {}
            }
        }
        """
        if not track_performance:
            return 0

        transaction_context = sampling_context.get("transaction_context")

        if transaction_context is None:
            return 0

        op = transaction_context.get("op")

        if op is None:
            return 0

        if op == "celery.task":
            return 0

        return 0.5

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=environment,
        traces_sampler=traces_sampler,
        integrations=[
            DjangoIntegration(),
            CeleryIntegration(),
        ],
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=False
    )

#!/bin/bash
echo "--> Starting beats process"
celery -A styleguide_example.tasks beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

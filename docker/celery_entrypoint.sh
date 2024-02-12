#!/bin/bash
echo "--> Starting celery process"
celery -A styleguide_example.tasks worker -l info --without-gossip --without-mingle --without-heartbeat

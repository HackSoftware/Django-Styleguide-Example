echo "--> Starting beats process"
celery -A styleguide_example.tasks worker -l info --without-gossip --without-mingle --without-heartbeat
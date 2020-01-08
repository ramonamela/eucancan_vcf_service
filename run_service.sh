#!/bin/bash

export FLASK_APP=/mnt/nfs/eucancan_vcf_vc/annotation_service/vca_service.py
export FLASK_ENV=development
listen_port=5000
flask run --host=0.0.0.0 --port=${listen_port}

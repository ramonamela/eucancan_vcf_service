#!/bin/bash

target_ip="84.88.186.194"

curl -X POST -F "vcf_file=@$(pwd)/test_files/test.txt" "http://${target_ip}:5000/files/"
curl -X POST -F "vcf_file=@$(pwd)/test_files/test.vcf.gz" "http://${target_ip}:5000/files/"
curl -X POST -F "vcf_file=@$(pwd)/test_files/test.vcf.gz" "http://${target_ip}:5000/files/"
curl -X GET "http://${target_ip}:5000/files/test.vcf.gz"
curl -X DELETE "http://${target_ip}:5000/files/test.vcf.gz"
curl -X DELETE "http://${target_ip}:5000/files/test.vcf.gz"


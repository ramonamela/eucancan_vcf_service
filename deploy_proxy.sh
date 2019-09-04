#!/bin/bash

input_ip=10.32.3.1
input_port=5000
service_port=5000
service_ip=10.32.3.2


#ssh ${input_ip} "python3 -u -- -ip ${input_port} -sp ${service_port} -sa ${service_ip}" < /mnt/nfs/eucancan_vcf_vc/proxy_flask/flask_proxy.py

#ssh ${input_ip} "python3 - -ip ${input_port} -sp ${service_port} -sa ${service_ip}" < /mnt/nfs/eucancan_vcf_vc/proxy_flask/flask_proxy.py 
#"--input_port" "${input_port}" "--service_port" "${service_port}" "--service_address" "${service_ip}"

#ssh ${input_ip} "python3 - --input_port ${input_port} --service_port ${service_port} --service_address ${service_ip}" < /mnt/nfs/eucancan_vcf_vc/proxy_flask/flask_proxy.py

ssh ${input_ip} "python3 -" < /mnt/nfs/eucancan_vcf_vc/proxy_flask/flask_proxy.py "--input_port ${input_port} --service_port ${service_port} --service_address ${service_ip}"

#ssh ${input_ip} "cat | python3 -u /dev/stdin" "--input_port ${input_port} --service_port ${service_port} --service_address ${service_ip}" < /mnt/nfs/eucancan_vcf_vc/proxy_flask/flask_proxy.py

#ssh ${input_ip} python3 -u -- < /mnt/nfs/eucancan_vcf_vc/proxy_flask/flask_proxy.py "--input_port ${input_port} --service_port ${service_port} --service_address ${service_ip}"



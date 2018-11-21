# jcdns
Simple DNS Proof of Concept in Python

Authorative name server intended for load balancing requests across different IPs.

Supports random choice, or percent of traffic as schedulers

python jcdns.py

dig abc.com @localhost

Usage: 
jcdns.py -f zones.json (path to zones JSON file)
jcdns.py -d (fork and detach process as daemon)



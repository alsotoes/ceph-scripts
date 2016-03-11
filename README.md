Let's see how it works ceph_space.py
=======

* TXT output (any of the tree options print the same output)


	$ python ceph_space.py "Ceph Cluster"  
	$ python ceph_space.py --output txt "Ceph Cluster"  
	$ python ceph_space.py --output txt --ratio 0.2 "Ceph Cluster"  
	
	 	Cluster codename: Ceph Cluster
	 	Cluster ID: 85289369-1173-44b9-8a4c-ab5c1b50270f
	 	Cluster mon to connect: stor01.ceph.local
	 	Cluster Statistics
	 		 	Total: 10.7TB
	 		 	Reserved: 2.1TB
	 		 	Usable (before warning): 8.5TB
	 		 	Used: 2.1TB
	 		 	
	 		 	Total Available: 6.5TB
	 		 	Percentage Available: 75%


* CSV print 

	$ python ceph_space.py --output csv --ratio 0.2 "Ceph Cluster"
	
	 	Cluster Name,Cluster ID,Cluster MON,Total,Reserved,Usable,Used,Available,Percentage Available
	 	Ceph Cluster,85289369-1173-44b9-8a4c-ab5c1b50270f,stor01.ceph.local,10.7TB,2.1TB,8.5TB,2.1TB,6.5TB,75%


* CSV printing and leaving a CSV file named cluster_stats (change with --file) in CWD

	$ python ceph_space.py --output csv --ratio 0.2 --file cluster_stats "Ceph Cluster"
	
	 	Cluster Name,Cluster ID,Cluster MON,Total,Reserved,Usable,Used,Available,Percentage Available
	 	Ceph Cluster,85289369-1173-44b9-8a4c-ab5c1b50270f,stor01.ceph.local,10.7TB,2.1TB,8.5TB,2.1TB,6.5TB,75%

	$ cat cluster_stats.csv

		Cluster Name,Cluster ID,Cluster MON,Total,Reserved,Usable,Used,Available,Percentage Available
		Ceph Cluster,85289369-1173-44b9-8a4c-ab5c1b50270f,stor01.ceph.local,10.7TB,2.1TB,8.5TB,2.1TB,6.5TB,75%

Let's see how it works
=======

* TXT output


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


* CSV output

	$ python ceph_space.py --output csv --ratio 0.2 "Ceph Cluster"
	
	 Cluster Name,Cluster ID,Cluster MON,Total,Reserved,Usable,Used,Available,Percentage Available
	 Ceph Cluster,85289369-1173-44b9-8a4c-ab5c1b50270f,stor01.ceph.local,10.7TB,2.1TB,8.5TB,2.1TB,6.5TB,75%

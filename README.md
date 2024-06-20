# quackers
First release: June 13, 2024

Parkinson Lab's in-house MG pipeline.
Setup:
Need to download a few databases:
https://github.com/Ecogenomics/CheckM/wiki/Installation#how-to-install-checkm
https://data.ace.uq.edu.au/public/CheckM_databases/

https://ecogenomics.github.io/GTDBTk/installing/index.html#installing-gtdbtk-reference-data
WARNING: it's 84GB, and you need to unzip it yourself.

Also: 
use the sample config, and assign the 2 databases entries to the paths.
special note for gtdbtk, use release220, and have the config point to it. 

Also: 
your host fastas need to be indexed by BWA before use.  else quackers will complain. 

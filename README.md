# Frames derived from S1-bursts

This is to generate a vector file that illustrates fixed frame for interferogram enumeration. This is a work in progress.

The burst maps are downloaded from ESA [page](https://sar-mpc.eu/test-data-sets/). We downloaded `S1_burstid_20220530`. We aggregate every 10 bursts ensuring 2 burst overlap when applicable. If bursts are have less than 8 bursts, we merge it with its neighbor that was acquired earlier (if possible). We consider bursts only over land as dictated by  `GSHHG` found [here](https://www.ngdc.noaa.gov/mgg/shorelines/data/gshhg/latest/) with a 1 degree buffer.

We also illustrate how to solve a potential dateline issue, though some discussion may be required for next steps.
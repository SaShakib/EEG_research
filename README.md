# EEG_research
To use this repository you first need to clone this using 
git clone https://github.com/SaShakib/EEG_research

If you have already recorded EEG data there are several files to visualize them and also get insights, like Eye/b.py if you edit this file and with your csv file and column names it will give you a visualization stream. 

if you want to communicate with live data, we are using muse 2. and it needs to be used with petal metrics software to stream the data. 
and on petal metric get started folder you have get the data through ocs server. 
to run the server use 

python -u lsl_receive.py -n PetalStream_eeg 

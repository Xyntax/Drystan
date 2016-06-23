# Drystan
#### Automated information gathering tool for pentest

*v0.4a by <i@cdxy.me>*


> "Begin to explore your truths, your story, and begin to look beneath the surface."
>  - Lucy Cavendish     

How It Works
------------
1. explore domain information. 
2. search and enumerate subDomains.
3. extract all IP & ports.
4. identify service.
5. detect vulnerability.


Quick Start
-----------
Drystan is written in Python 2.7 and needs some tools/projects/modules, please install all dependencies first:
`python install.py` 

It can be run from any unix/Linux machine, best run from Kali-Linux.
`python drystan.py -h`

You can modify the system settings manually by editing the config file:
`vi config.py`
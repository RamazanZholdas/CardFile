#!/bin/bash
APPLICATION_NAME=$1
DOCUMENT_ROOT=$2
####################APACHE PROXY CONF##################
sudo printf 'Listen 8080\n' >> /etc/httpd/conf.d/proxy.conf
sudo echo 'LogFormat "%h (%{X-Forwarded-For}i) %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined' >> /etc/httpd/conf.d/proxy.conf
sudo printf '\nSetOutputFilter DEFLATE' >> /etc/httpd/conf.d/proxy.conf
sudo printf '\nProxyPreserveHost On\n' >> /etc/httpd/conf.d/proxy.conf
sudo printf "\nProxyPass $APPLICATION_NAME http://127.0.0.1:8081/" >> /etc/httpd/conf.d/proxy.conf
sudo printf "\nProxyPassReverse $APPLICATION_NAME http://127.0.0.1:8081/" >> /etc/httpd/conf.d/proxy.conf
##################APACHE CONF/HARDENING#################
sudo sed -i "s_DocumentRoot \"/var/www/html\"_DocumentRoot \"$DOCUMENT_ROOT\"_g" /etc/httpd/conf/httpd.conf
sudo sed -i 's_Listen 80_ _g' /etc/httpd/conf/httpd.conf
####################HEADERS AND SO ON###################
sudo printf "\nSetEnv force-proxy-request-1.0 1\n" >> /etc/httpd/conf/httpd.conf
sudo printf "\nSetEnv proxy-nokeepalive 1\n" >> /etc/httpd/conf/httpd.conf
#####################APACHE MODULES##################### <-------------- MODULES HAVE BEEN REPLACED to /etc/httpd/conf.modules.d/**
sudo sed -i "s_LoadModule auth\_basic\_module modules/mod\_auth\_basic.so_#LoadModule auth\_basic\_module modules/mod\_auth\_basic.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule auth\_digest\_module modules/mod\_auth\_digest.so_#LoadModule auth\_digest\_module modules/mod\_auth\_digest.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule authn\_file\_module modules/mod\_authn\_file.so_#LoadModule authn\_file\_module modules/mod\_authn\_file.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule authn\_alias\_module modules/mod\_authn\_alias.so_#LoadModule authn\_alias\_module modules/mod\_authn\_alias.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule authn\_anon\_module modules/mod\_authn\_anon.so_#LoadModule authn\_anon\_module modules/mod\_authn\_anon.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule authn\_dbm\_module modules/mod\_authn\_dbm.so_#LoadModule authn\_dbm\_module modules/mod\_authn\_dbm.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule authn\_default\_module modules/mod\_authn\_default.so_#LoadModule authn\_default\_module modules/mod\_authn\_default.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule authz\_user\_module modules/mod\_authz\_user.so_#LoadModule authz\_user\_module modules/mod\_authz\_user.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule authz\_owner\_module modules/mod\_authz\_owner.so_#LoadModule authz\_owner\_module modules/mod\_authz\_owner.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule authz\_groupfile\_module modules/mod\_authz\_groupfile.so_#LoadModule authz\_groupfile\_module modules/mod\_authz\_groupfile.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule authz\_dbm\_module modules/mod\_authz\_dbm.so_#LoadModule authz\_dbm\_module modules/mod\_authz\_dbm.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule ldap\_module modules/mod\_ldap.so_#LoadModule ldap\_module modules/mod\_ldap.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule authnz\_ldap\_module modules/mod\_authnz\_ldap.so_#LoadModule authnz\_ldap\_module modules/mod\_authnz\_ldap.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule include\_module modules/mod\_include.so_#LoadModule include\_module modules/mod\_include.so_g" /etc/httpd/conf/httpd.conf
#sudo sed -i "s_LoadModule env\_module modules/mod\_env.so_#LoadModule env\_module modules/mod\_env.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule ext\_filter\_module modules/mod\_ext\_filter.so_#LoadModule ext\_filter\_module modules/mod\_ext\_filter.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule mime\_magic\_module modules/mod\_mime\_magic.so_#LoadModule mime\_magic\_module modules/mod\_mime\_magic.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule expires\_module modules/mod\_expires.so_#LoadModule expires\_module modules/mod\_expires.so_g" /etc/httpd/conf/httpd.conf
#sudo sed -i "s_LoadModule deflate\_module modules/mod\_deflate.so_#LoadModule deflate\_module modules/mod\_deflate.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule usertrack\_module modules/mod\_usertrack.so_#LoadModule usertrack\_module modules/mod\_usertrack.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule dav\_module modules/mod\_dav.so_#LoadModule dav\_module modules/mod\_dav.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule status\_module modules/mod\_status.so_#LoadModule status\_module modules/mod\_status.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule autoindex\_module modules/mod\_autoindex.so_#LoadModule autoindex\_module modules/mod\_autoindex.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule info\_module modules/mod\_info.so_#LoadModule info\_module modules/mod\_info.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule dav\_fs\_module modules/mod\_dav\_fs.so_#LoadModule dav\_fs\_module modules/mod\_dav\_fs.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule vhost\_alias\_module modules/mod\_vhost\_alias.so_#LoadModule vhost\_alias\_module modules/mod\_vhost\_alias.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule negotiation\_module modules/mod\_negotiation.so_#LoadModule negotiation\_module modules/mod\_negotiation.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule actions\_module modules/mod\_actions.so_#LoadModule actions\_module modules/mod\_actions.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule speling\_module modules/mod\_speling.so_#LoadModule speling\_module modules/mod\_speling.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule userdir\_module modules/mod\_userdir.so_#LoadModule userdir\_module modules/mod\_userdir.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule alias\_module modules/mod\_alias.so_#LoadModule alias\_module modules/mod\_alias.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule substitute\_module modules/mod\_substitute.so_#LoadModule substitute\_module modules/mod\_substitute.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule proxy\_balancer\_module modules/mod\_proxy\_balancer.so_#LoadModule proxy\_module modules/mod\_proxy.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule proxy\_ftp\_module modules/mod\_proxy\_ftp.so_#LoadModule proxy\_ftp\_module modules/mod\_proxy\_ftp.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule proxy\_ajp\_module modules/mod\_proxy\_ajp.so_#LoadModule proxy\_ajp\_module modules/mod\_proxy\_ajp.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule cache\_module modules/mod\_cache.so_#LoadModule cache\_module modules/mod\_cache.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule suexec\_module modules/mod\_suexec.so_#LoadModule suexec\_module modules/mod\_suexec.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule disk\_cache\_module modules/mod\_disk\_cache.so_#LoadModule disk\_cache\_module modules/mod\_disk\_cache.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule cgi\_module modules/mod\_cgi.so_#LoadModule cgi\_module modules/mod\_cgi.so_g" /etc/httpd/conf/httpd.conf
sudo sed -i "s_LoadModule version\_module modules/mod\_version.so_#LoadModule version\_module modules/mod\_version.so_g" /etc/httpd/conf/httpd.conf
####################TURNING OFF TRASH###################
sudo sed -i 's_ScriptAlias /cgi-bin/ \"/var/www/cgi-bin/\"_#ScriptAlias /cgi-bin/ \"/var/www/cgi-bin/\"_g' /etc/httpd/conf/httpd.conf
sudo sed -i "s_Alias /error/ \"/var/www/error/\"_#Alias /error/ \"/var/www/error/\"_g" /etc/httpd/conf/httpd.conf #<--------- NOT FOUND
sudo sed -i "s_Alias /icons/ \"/var/www/icons/\"_#Alias /icons/ \"/var/www/icons/\"_g" /etc/httpd/conf/httpd.conf  #<--------- NOT FOUND
sudo sed -i "s_IndexOptions FancyIndexing_#IndexOptions FancyIndexing_g" /etc/httpd/conf/httpd.conf #<--------- NOT FOUND
sudo sed -i "s_AddIcon_#AddIcon_g" /etc/httpd/conf/httpd.conf #<--------- NOT FOUND
sudo sed -i "s_DefaultIcon_#DefaultIcon_g" /etc/httpd/conf/httpd.conf   #<--------- NOT FOUND
sudo sed -i "s_ForceLanguagePriority_#ForceLanguagePriority_g" /etc/httpd/conf/httpd.conf     #<--------- NOT FOUND
sudo sed -i "s_LanguagePriority_#LanguagePriority_g" /etc/httpd/conf/httpd.conf     #<--------- NOT FOUND
sudo sed -i "s_ReadmeName README.html_#ReadmeName README.html_g" /etc/httpd/conf/httpd.conf      #<--------- NOT FOUND
sudo sed -i "s_IndexIgnore_#IndexIgnore_g" /etc/httpd/conf/httpd.conf     #<--------- NOT FOUND
sudo sed -i "s_HeaderName HEADER.html_#HeaderName HEADER.html_g" /etc/httpd/conf/httpd.conf     #<--------- NOT FOUND
####################HEADERS AND SO ON###################
sudo printf '\nServerSignature Off\n' >> /etc/httpd/conf/httpd.conf
sudo printf '\nServerTokens ProductOnly\n' >> /etc/httpd/conf/httpd.conf
sudo printf '\nHeader always append X-Frame-Options SAMEORIGIN\n' >> /etc/httpd/conf/httpd.conf
sudo printf '\nHeader set X-XSS-Protection \"1; mode=block\"\n' >> /etc/httpd/conf/httpd.conf
sudo printf '\nHeader set Strict-Transport-Security \"max-age=31536000; includeSubDomains; preload\"\n' >> /etc/httpd/conf/httpd.conf
sudo printf '\nHeader set X-Content-Type-Options nosniff\n' >> /etc/httpd/conf/httpd.conf
sudo printf '\nHeader set X-Powered-By EDETEK\n' >> /etc/httpd/conf/httpd.conf
sudo printf '\nHeader set Server EDETEK\n' >> /etc/httpd/conf/httpd.conf
sudo printf '\nHeader unset ETag\n' >> /etc/httpd/conf/httpd.conf
sudo printf '\nFileETag None\n' >> /etc/httpd/conf/httpd.conf
#sudo printf "\nHeader set Content-Security-Policy \"frame-ancestors 'self';\"\n" >> /etc/httpd/conf/httpd.conf
sudo printf "\nHeader set Content-Security-Policy \"frame-ancestors https://COMMON_UI_URL_VAR https://COMMON_API_URL_VAR;\"\n" >> /etc/httpd/conf/httpd.conf
####################TUNING###################
cat >> /etc/httpd/conf/httpd.conf << EOF
<IfModule mpm_prefork_module>
    ServerLimit 1500
    MaxRequestWorkers 1300
</IfModule>
EOF
####################DEFLATE###################
#sudo sed -i '/<Directory \"\/var\/www\/html\">/a \
#<IfModule mod_mime.c> \
# AddType application/x-javascript .js \
# AddType text/css .css \
#</IfModule> \
#<IfModule mod_deflate.c> \
# # Compress HTML, CSS, JavaScript, Text, XML and fonts \
# AddOutputFilterByType DEFLATE application/javascript \
# AddOutputFilterByType DEFLATE application/rss+xml \
# AddOutputFilterByType DEFLATE application/vnd.ms-fontobject \
# AddOutputFilterByType DEFLATE application/x-font \
# AddOutputFilterByType DEFLATE application/x-font-opentype \
# AddOutputFilterByType DEFLATE application/x-font-otf \
# AddOutputFilterByType DEFLATE application/x-font-truetype \
# AddOutputFilterByType DEFLATE application/x-font-ttf \
# AddOutputFilterByType DEFLATE application/x-javascript \
# AddOutputFilterByType DEFLATE application/xhtml+xml \
# AddOutputFilterByType DEFLATE application/xml \
# AddOutputFilterByType DEFLATE font/opentype \
# AddOutputFilterByType DEFLATE font/otf \
# AddOutputFilterByType DEFLATE font/ttf \
# AddOutputFilterByType DEFLATE image/svg+xml \
# AddOutputFilterByType DEFLATE image/x-icon \
# AddOutputFilterByType DEFLATE text/css \
# AddOutputFilterByType DEFLATE text/html \
# AddOutputFilterByType DEFLATE text/javascript \
# AddOutputFilterByType DEFLATE text/plain \
# AddOutputFilterByType DEFLATE text/xml \
# #The following line is enough for .js and .css \
# AddOutputFilter DEFLATE js css \
# AddOutputFilterByType DEFLATE text/plain text/xml application/xhtml+xml text/css application/javascript application/xml application/rss+xml application/atom_xml application/x-javascript application/x-httpd-php application/x-httpd-fastphp text/html \
#</IfModule> \
#<IfModule mod_setenvif.c> \
# # Old Browsers \
# BrowserMatch ^Mozilla/4 gzip-only-text/html \
# BrowserMatch ^Mozilla/4\.0[678] no-gzip \
# BrowserMatch \bMSIE !no-gzip !gzip-only-text/html \
#</IfModule> \
#<IfModule mod_gzip.c> \
# mod_gzip_on Yes \
# mod_gzip_dechunk Yes \
# mod_gzip_item_include file .(html?|txt|css|js|php|pl)$ \
# mod_gzip_item_include handler ^cgi-script$ \
# mod_gzip_item_include mime ^text/.* \
# mod_gzip_item_include mime ^application/x-javascript.* \
# mod_gzip_item_exclude mime ^image/.* \
# mod_gzip_item_exclude rspheader ^Content-Encoding:.*gzip.* \
#</IfModule>' /etc/httpd/conf/httpd.conf
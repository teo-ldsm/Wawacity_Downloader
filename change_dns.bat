netsh interface ip set dns name="%1" static 8.8.8.8
netsh interface ipv4 add dnsservers "%1" 8.8.4.4 index=2
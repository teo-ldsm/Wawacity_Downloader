netsh interface ip set dns name="%1" static 8.8.8.8
netsh interface ipv4 add dnsservers "%1" 8.8.4.4 index=2
netsh interface ipv6 set dns name="%1" static 2001:4860:4860::8888
netsh interface ipv6 add dnsservers "%1" 2001:4860:4860::8844 index=2
setx HTTP_PROXY http://proxy.wdf.sap.corp:8080
setx HTTPS_PROXY http://proxy.wdf.sap.corp:8080
setx FTP_PROXY http://proxy.wdf.sap.corp:8080
setx ALL_PROXY http://proxy.wdf.sap.corp:8080
setx NO_PROXY localhost,127/8,*.local,169.254/16,*.sap.corp,*.corp.sap,.sap.corp,.corp.sap
setx MAVEN_OPTS "-Dhttp.proxyHost=proxy.wdf.sap.corp -Dhttp.proxyPort=8080 -Dhttps.proxyHost=proxy.wdf.sap.corp -Dhttps.proxyPort=8080 -Dhttps.proxyHost=proxy.wdf.sap.corp -Dhttps.proxyPort=8080 -Dhttp.nonProxyHosts=localhost^|127.*^|[::1]^|*.sap.corp"
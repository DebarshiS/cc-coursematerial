#!/bin/bash -e

space=refapp-production
appRouterUrl=https://bulletinboard-approuter-$space.cfapps.sap.hana.ondemand.com
serviceKeyGuid=$(cf service-key --guid uaa-bulletinboard testServiceKey)
serviceKeyJson=$(cf curl /v2/service_keys/$serviceKeyGuid)
cookieFile=cookie-jmeter.txt

clientId=$(echo ${serviceKeyJson} | jq -r ".entity.credentials.clientid")
echo "Read clientId $clientId"
clientSecret=$(echo ${serviceKeyJson} | jq -r ".entity.credentials.clientsecret")
xsAppName=$(echo ${serviceKeyJson} | jq -r ".entity.credentials.xsappname")

jsonData="{ \"uaaURL\": \"https://d012345trial.authentication.sap.hana.ondemand.com\", \"clientID\": \"${clientId}\",	\"clientSecret\": \"${clientSecret}\",	\"username\": \"testuser\",	\"samlAttributes\": {		\"Groups\": [\"RC_Bulletinboard\"] }, \"redirectURI\":\"${appRouterUrl}/login/callback\" }"

echo "Content $jsonData"

HTTP_RESPONSE=$(curl -f -H "Content-Type: application/json" -X POST -d "$jsonData" 'https://xsuaa-monitoring-idp.cfapps.sap.hana.ondemand.com/getauthcode')
echo "Got http response $HTTP_REPONSE"

authCode=$(echo $HTTP_RESPONSE | jq -r ".authCode")

echo "Got auth code $authCode"

rm -f $cookieFile

echo "Request to $appRouterUrl/login/callback?code=$authCode"

curl -f -L -H "Referer: https://accounts.sap.com" -H "Cookie: locationAfterLogin=/" -c $cookieFile "$appRouterUrl/login/callback?code=$authCode"

echo $?

cat $cookieFile

jsessionId=$(cat $cookieFile | grep JSESSIONID | cut -f7 -d$'\t')

rm -f $cookieFile

echo "JSESSIONID: ${jsessionId}"



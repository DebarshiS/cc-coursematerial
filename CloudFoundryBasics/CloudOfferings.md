# Cloud Offerings - Background on terminology and semantics

## SAP (public) Cloud Platforms - 2017

<img src="https://github.com/ccjavadev/cc-coursematerial/blob/master/Z_ReuseImages/images/CloudOfferings.png" width="900" />


## XSA - XS Advanced

From a simplistic view, the runtime platform of [XSA](https://wiki.wdf.sap.corp/wiki/display/xs2/Home) is a SAP proprietary, trimmed-down Cloud Foundry fork for developing and running HANA-based web applications, that runs also on customer hosted systems without Cloud Foundry setup, without the need for an additional application server. In addition XSA provides standard services, e.g. job scheduling, multi-tenancy, compatibility layer for (old) XSJS applications of HANA XS. A lot of the libraries and components (backing services) that are provided by XSA are also useful for JAVA / Node.JS applications running on a plain CP Cloud Foundry. 

XSA is also often referred to as "XSA (on) Cloud Foundry", formerly also known as (aka.):
* SAP HANA Cloud 
* SAP Netweaver Cloud / Neo / OnDemand
* Java Platform as a Service (JPaaS)
* Project "River"

To make the naming-confusion perfect, the terms "XSA" and "XS2" are used interchageably: The term "XS2" was derived from "XS1" resp. "HANA XS", the HANA eXtended Services, and later renamed to "XSA". HANA XS is tighly bound with the HANA database and thereby extending it with a JavaScript runtime to also serve as an application server. XSA is not tighly bound with the HANA database and can host multiple runtimes, e.g. Java, Node.js, Ruby, etc.

Have a look into the [SAP Hana Developer Guide for XSA](https://help.sap.com/viewer/4505d0bdaf4948449b7f7379d24d0f0d/2.0.00/en-US/f472017c780e4db4adcbccc8ba04de05.html)

## Platform capabilities
Before making your platform decision you should know your business case very well, having a clear strategy on how to earn money for example (read more about that [here](https://sapedia.wdf.sap.corp/wiki/Business_Model_Canvas)). On that base you might be able to derive the business and technical capabilities required and to do the right platform decision.

Some criterias
- delivery model: cloud and/or on-premise
- UI: Fiori/SAP UI5 or freestyle UI or RestAPI only
- Scalability
- Required services like HANA Cloud Connector / Integration
- Technology stack

### Positioning of SAP CP Cloud Foundry versus Neo
- [Detailed Positioning and Dev Guideline for SAP CP Cloud Foundry versus Neo](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/blob/master/Knowledge/HCP_CF%40HCP_Application_Provider_final.pdf)
- Have a look at the [One CP Platform Guide](https://wiki.wdf.sap.corp/wiki/display/ONEHCP/Platform+Guide)  

## Further references
- [SAP CP Neo vs. Cloud Foundry value proposition](https://wiki.wdf.sap.corp/wiki/display/ONEHCP/Value+Proposition)
- [SAP CP Platform Guide](https://wiki.wdf.sap.corp/wiki/display/ONEHCP/Platform+Guide)
- [SAP CP and Cloud Foundry Strategy for customers (SCN)](http://scn.sap.com/community/developer-center/cloud-platform/blog/2016/05/31/the-road-ahead-with-sap-hana-cloud-platform-and-cloud-foundry--sap-teched-strategy-talk-of-the-week)
- [YaaS marketplace](https://market.yaas.io/standard)


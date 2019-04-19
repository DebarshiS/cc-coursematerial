# Open Source Notes

Starting with december 2016 there is a new Open Source process ([details about the process](https://wiki.wdf.sap.corp/wiki/display/glwikilc/New+FOSS+Validation+Process)) available where you do not need to create requests in Code Center anymore. You basically have to check if a component is already risk-rated via https://open-source.mo.sap.corp/ and then ask your PPMS entry owner to add the respective FOSS objects to the product.

Depending on the respective delivery channel / program, processes for adding new Open Source may vary, therefore best contact would be the program/delivery manager.

### Glossary:
- A **component** is a specific artifact of open source software that is uniquely identified by its name and version following the naming convention from the provider, e.g.: Apache Tomcat 8.0.32.
- An **application** is an object in CodeCenter that represents a SAP product, which is identified by its program name in the Program Repository or Sirius.

#### Which version should be used?
In general it is recommended to use the latest version available. Only in the case of incompatible changes older versions should be used.

#### Which component? 
For certain components it is not necessary to reference the exact component.
Instead, the "parent" component can be used.
In our settings this applies to several Spring components which are represented in the "Spring Framework" component.
The Maven group ID (`org.springframework`) can be helpful to identify such umbrella projects.

Only direct dependencies need to be declared in your PPMS model. The PPMS model has to contain all so-called FOSS objects which are in direct use. Direct means that you are directly calling the respective API and not indirectly. An example for an indirect usage would be JQuery via UI5: if you only use UI5 APIs (which in the background use JQuery) you only need to declare UI5 usage.


#### Which components need to be approved?
According to the Code Center team, also components used only for **tests and builds** need to be approved. **SAP components** i.e. libraries developed by SAP like the logging libary, can be used without approval.
A good way to identify SAP components is to ensure that SAP holds the copyright.


#### Components without a product
Usually each component needs to be assigned to a product.
In the case of the Cloud Curriculum, where no such product exists, it is also possible to assign components to the `#Non Product Specific Tools & Utilities ("P&I" and "BN-Business Network" ONLY)#.`


## Related Links
- [New FOSS Validation Process](https://wiki.wdf.sap.corp/wiki/display/GTLC/Code+Center+User+Guide)
- [UI to search for, request and declare usage of FOSS](https://open-source.mo.sap.corp).

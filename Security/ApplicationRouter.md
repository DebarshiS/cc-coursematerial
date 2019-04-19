# Application Router Notes

- Simplifies the authentication
- Allows to define start/stop conditions, i.e. ensures whether the user is allowed to access the service
- Protects against [Cross-Site-Request-Forgery](https://de.wikipedia.org/wiki/Cross-Site-Request-Forgery)
- External users ("the browser") access internal applications using an URL of the application router, extended by a path describing the application destination (example: https://url-of-approuter/xyz/ to access application xyz). This mapping is specified in `xs-app.json`.


### Technical Impacts
- Each instance of the application router stores the JWT information in memory, i.e. for multiple instances session stickiness should be used
- The application router is a JavaScript application => redundancy/HA needs to be ensured
- In CF there is no private communication between applications. This means that the application router communicates with the "real" applications using publicly visible URLs, that are known to the CF router. The applications should only allow connections containing a JWT token (coming from the application router). Note: Only Backing Services can be "private" i.e.: not externally accessible via URL.
- Different applications making use of different rules/authorizations should not use the same application router! Each application router provides all user roles in the corresponding JWT token, meaning that an application that is served by the same app router might misuse the JWT token to do unallowed calls. In that context consider also, that the JWT is a HTTP Header information that has some size limitations.
- After a crash the frontend application (UI5 etc.) should re-establish the session gracefully without resetting state or redirecting to the login page

## In the Future...
- it might be possible to run applications like the application router as a dedicated service, see "Routing Extensions" in [this document](https://www.activestate.com/blog/2015/02/cloud-foundry-advisory-board-meeting-2015-february
- approuter will be multi-tenant aware, will pass tenant information to the application, that needs to react on that information
- There will be a working Admin UI to maintain the user, roles

## Further Links
- [Wiki](https://wiki.wdf.sap.corp/wiki/display/xs2/Approuter+Architecture)
- [Approuter Presentation](https://wiki.wdf.sap.corp/wiki/display/xs2/Approuter+Architecture?preview=/1815947157/1815947197/XS2%20Application%20Router%20-%20Diagrams.pptx)
- [Git Repository](https://github.wdf.sap.corp/xs2/approuter.js/blob/master/README.md)

## Random notes:
 - SIC is "Siemens Industry Cloud", has a multi-tenant enabled app router
 - SAP CP Industry Edition more or less is identical to the Canary landscape
 - Persisting this information, for example using Redis, is not desired for security reasons
 - For the training its recommended to order another Identity Provider (IDP) instance, that can be cleaned up after the training
 - SAP Identity Service is only used for Business Application User (that is a tenant of Cloud Identity Service)

# Create an API Documentation using Swagger/SpringFox

## Motivation
An API must expose proper metadata that describes each entity and its fields, as well as operations and
types, using the metadata mechanism of the chosen API protocol Swagger for REST APIs.

In addition and to provide further guidance to the consumers of the API, a documentation is required to
explain the use cases the API was designed for. Each use case shall be documented with at least one
example. Such documentation can be placed on any publicly accessible web host, as long it is linked from
the [Content Hub](https://api.sap.com/) listing. Documentation must exist for every published version of the API.

For each API there must be either a link to a publicly reachable API documentation or alternatively, you can document your API in the Content Hub when you make use of protocols such as Swagger or OData, ...

**Extract from the [CTO Circle whitepaper `Application Integration Direction`](https://jam4.sapjam.com/wiki/show/eBIJTH4EwfD15ymE2nv2pG)**
> All API methods documented in the Content Hub should either serve a single resource or a single action. If
multiple actions can be invoked from a single generic API method by submitting different message data the
API method must either be broken down or each invocation shall be documented separately.

> API providers must describe every API method and every field of the input and output messages of an API
method. This is to be conducted transitively for all complex types used in fields.
API providers should submit examples for all major use cases of their APIs. Every API must have at least
one example of the primary use case it has been designed for.

An example of the implementation can be found in the Spring Boot Bulletinboard [GitHub Repository](https://github.wdf.sap.corp/cc-refapp/cc-bulletinboard-ads-spring-boot/tree/api-documentation). 

## Tools Used

#### Swagger™ (Open API)
Swagger is a project used to describe and document RESTful APIs. It wants to allow both humans and computers to discover and understand the capabilities of the service without access to source code, documentation, or through network traffic inspection. 

#### Springfox
In context of Spring application you can make use of [`Springfox`](http://springfox.github.io/springfox/) to expose Swagger API documentation for API's built with Spring.

#### Swagger UI
If there is a Swagger API documentation, [Swagger UI](https://swagger.io/swagger-ui/) allows consumers to interact with the API’s resources.

## Expose Swagger documentation for your REST API
### Add Maven dependencies
In order to setup SpringFox for Swagger API documentation you need to include the following dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>io.springfox</groupId>
    <artifactId>springfox-swagger2</artifactId>
    <version>2.5.0</version>
</dependency>
```
([Open Source - Licensing Risks and Security Vulnerabilities](https://open-source.mo.sap.corp/springfox))

The dependency `springfox-swagger2` loads the Swagger core which is responsible for producing a `JSON` file containing the API documentation. This documentation can later be accessed via the following route:

```http://<host>:<port>/v2/api-docs```

### Configuration

Before the documentation can be generated and examined via the Swagger UI, Swagger has to be properly configured using Java code.
A quick guide on how to do that can be found here: http://www.baeldung.com/swagger-2-documentation-for-spring-rest-api

A more verbose version is provided by the official documentation which is accessible here: https://springfox.github.io/springfox/docs/current/

If you want to add custom elements to your JSON documentation (e. g. you want to mark a specific endpoint as a beta version),
a Swagger `BuilderPlugin` must be implemented.

### OperationBuilderPlugin

If you want to include custom method annotations into your API documentation you have to implement an `OperationBuilderPlugin`
telling Swagger how to handle this kind of annotations. In the example a `@Beta` annotation is created which is used to annotate methods/endpoints which are still in the testing phase and not yet productive. This kind of information is crucial in an API documentation therefore it should be included therein. This is why an `IsBetaOperationBuilderPlugin` is implemented.

This `IsBetaOperationBuilderPlugin`, which implements the `OperationBuilderPlugin` interface provided by the Swagger core contains a method called `apply`. This method is executed each time a method to be documented was found and checks if it is annotated with the `@Beta` annotation. If yes it sets the `isBeta` flag to true and false otherwise. This flag is now available in the JSON produced. The following code snippet shows the implementation of the `OperationBuilderPlugin`:

```java
private class IsBetaOperationBuilderPlugin implements OperationBuilderPlugin {
        
   /**
    * Method to indicate which of the DocumentationTypes are supported.
    *
    * @param delimiter the documentation type to be checked.
    * @return true if the documentation type is supported, false if not.
    */
    @Override
    public boolean supports(DocumentationType delimiter) {
        return delimiter == DocumentationType.SWAGGER_2;
    }
        
    @Override
    public void apply(OperationContext context) {
        boolean isBeta = false;
           
        // check if the current method is annotated with @Beta
        if(context.getHandlerMethod().getMethod().isAnnotationPresent(Beta.class)) {
            isBeta = true;
        }
            
        // add isBeta entry to documentation
        context.operationBuilder().extensions(
            Collections.singletonList(
                new StringVendorExtension("isBeta", Boolean.toString(isBeta))
            )
        );
    }
}
```

After implementing the Plugin you have to register an instance of it as a bean:

```java
@Bean
public IsBetaOperationBuilderPlugin isBetaOperationBuilderPlugin() {
    return new IsBetaOperationBuilderPlugin();
}
```

### PropertyBuilderPlugin

Custom annotations can also be useful for model (entity) properties. For that you have to provide a class which
implements the `ModelPropertyBuilderPlugin` as shown below. In this example a `@ReadOnlyProperty` was created which indicates
that a member variable is not writable. Each property is then checked for that annotation and a flag is set accordingly.

```java
private class ReadOnlyPropertyBuilderPlugin implements ModelPropertyBuilderPlugin {
        
   /**
    * Method to indicate which of the DocumentationTypes are supported.
    *
    * @param delimiter the documentation type to be checked.
    * @return true if the documentation type is supported, false if not.
    */
    @Override
    public boolean supports(DocumentationType delimiter) {
        return delimiter == DocumentationType.SWAGGER_2;
    }
        
    @Override
    public void apply(ModelPropertyContext context) {
        ModelPropertyBuilder builder = context.getBuilder();
        AnnotatedField field = context.getBeanPropertyDefinition().get().getField();
            
        if(field != null) {
            ReadOnlyProperty readOnlyProperty = field.getAnnotation(ReadOnlyProperty.class);
            
            // check if it is annotated with @ReadOnlyProperty
            if(readOnlyProperty != null) {
                builder.readOnly(true);                    
            }
        }
    }
}
```

Also here you have to register a bean as described above.

A list of supported plugins is available here: https://github.com/springfox/springfox/blob/master/docs/asciidoc/extensibility.adoc

### Advanced Configurations and Settings

Some advanced configurations and settings (e. g. multiple Swagger groups, customization of Swagger UI, etc.) 
can be found here:
https://github.com/indrabasak/swagger-deepdive/wiki

## Swagger UI

### Setup

In most cases the `JSON` generated/`YAML` documentation is not sufficient and the need for a nice user interface arises.
To find a remedy for that the Swagger UI is put in the classpath (added as dependency in the `pom.xml`). This registers a new route:

```xml
<dependency>
    <groupId>io.springfox</groupId>
    <artifactId>springfox-swagger-ui</artifactId>
    <version>2.5.0</version>
</dependency>
```

```http://<host>:<port>/swagger-ui.html```

### Local Installation and Customizing

If you have added custom annotations to your documentation then they will not be displayed in the `Swagger UI`. For that you have to adapt it manually by changing its source code directly. The source code of the user interface can be downloaded from GitHub:
https://github.com/swagger-api/swagger-ui. After the download has completed copy the project directory into the `static` folder of your Spring Boot application. You can now access the Swagger UI from your `localhost`, e. g.:

```
http://localhost:8080/swagger-ui/dist/index.html
```

The user interface should now display the default petshop API. To change that, open the `index.html` file in a code editor of your choice. At the very bottom of the file you should find the following JavaScript code:

```javascript
<script>
    window.onload = function() {
  
        // Build a system
        const ui = SwaggerUIBundle({
            url: "http://petstore.swagger.io/v2/swagger.json",
            dom_id: "#swagger-ui",
            deepLinking: true,
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIStandalonePreset
            ],
            plugins: [
                SwaggerUIBundle.plugins.DownloadUrl
            ],
            layout: "StandaloneLayout"
        });

        window.ui = ui;
    }
</script>
```

Replace the `url` with

```javascript
location.protocol+ "//" + location.hostname + (location.port ? ":" + location.port: "8080") + "/v2/api-docs"
```

to point the Swagger UI to the JSON file of your own API which is produced by the Swagger core library.
Now it is possible to adapt the user interface to your needs. Please see this link for further information:
https://swagger.io/docs/swagger-tools/#swagger-ui-documentation-29

Since you have now added your custom implementation you can remove the Swagger UI dependency from the `pom.xml` file:

```diff
<dependency>
    <groupId>io.springfox</groupId>
    <artifactId>springfox-swagger-ui</artifactId>
    <version>2.5.0</version>
</dependency>
```

## API First Approach
Swagger can be used as an API definition language, so you start with the API design and implement the REST API afterwards. To generate the API documentation you need to create a `YAML` file containing the API description. The following sections provide some insights into that.

### Create YAML File

In order to create a `YAML` file, Swagger offers the `Swagger Editor` which is also available as a [web version](http://editor.swagger.io/). It also contains a sample Petshop API which can be used as a reference:

```yaml
swagger: "2.0"
info:
  description: "This is a sample server Petstore server."
  version: "1.0.0"
  title: "Swagger Petstore"
  termsOfService: "http://swagger.io/terms/"
  contact:
    email: "apiteam@swagger.io"
  license:
    name: "Apache 2.0"
    url: "http://www.apache.org/licenses/LICENSE-2.0.html"
host: "petstore.swagger.io"
basePath: "/v2"
tags:
- name: "pet"
  description: "Everything about your Pets"
  externalDocs:
    description: "Find out more"
    url: "http://swagger.io"
- name: "store"
  description: "Access to Petstore orders"
- name: "user"
  description: "Operations about user"
  externalDocs:
    description: "Find out more about our store"
    url: "http://swagger.io"
schemes:
- "http"
paths:
  /pet:
    post:
      tags:
      - "pet"
      summary: "Add a new pet to the store"
      description: ""
      operationId: "addPet"
      consumes:
      - "application/json"
      - "application/xml"
      produces:
      - "application/xml"
      - "application/json"
      parameters:
      - in: "body"
        name: "body"
        description: "Pet object that needs to be added to the store"
        required: true
        schema:
          $ref: "#/definitions/Pet"
      responses:
        405:
          description: "Invalid input"
      security:
      - petstore_auth:
        - "write:pets"
        - "read:pets"
        ...
```

### Create Mock Server/Mock Client

The interesting part of the API First approach is that it is possible to create mock servers and mock clients according to your API specification. For that the `Swagger Editor` offers special functionalities. In order to generate a mock server click on `Generate Server` in the menu of the `Swagger Editor`. You can now choose the programming language/framework which should be used. The same is possible for mock clients. For that just click on the menu item `Generate Client`. The generated source code is now available as a download.

There are also other tools available that are capable of creating a mock server/client automatically. For example `swagger-codegen`.

Additional information can also be found in the corresponding [issue 504](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/issues/504). 

## Further Reading
- [SAP API Business Hub](https://api.sap.com/)
- **General Configuration:**  
  - [Official Springfox Documentation](https://springfox.github.io/springfox/docs/current/)
  - [Basic Swagger Configuration](http://www.baeldung.com/swagger-2-documentation-for-spring-rest-api)
  - [More about Swagger Configuration](https://springframework.guru/spring-boot-restful-api-documentation-with-swagger-2/)
  - [Advanced Configuration of Swagger/Springfox](https://github.com/indrabasak/swagger-deepdive/wiki)
  - [Springfox GitHub Repo](https://github.com/springfox/springfox)
- **Swagger Plugins:**  
  - [Implementing Swagger Extensions using Plugins](https://homeadvisor.tech/api-documentation-swagger-extensions/)
  - [List of Plugins supported](https://github.com/springfox/springfox/blob/master/docs/asciidoc/extensibility.adoc)
  - [Internal: Example ReadOnlyPropertyBuilder](https://github.wdf.sap.corp/finliving/finliving/blob/master/backend/src/main/java/com/sap/finliving/common/swagger/ReadOnlyPropertyBuilderPlugin.java)
- **Swagger UI**  
  - [Install Swagger UI manually/Customization](https://swagger.io/docs/swagger-tools/#swagger-ui-documentation-29)
  - [Customize Swagger UI](https://github.com/domaindrivendev/Swashbuckle/wiki/3-Customizing-the-swagger-ui)  
- **Swagger Editor**  
  - [Swagger Editor](http://editor.swagger.io/)  
  - [Swagger Editor YAML](https://de.slideshare.net/fehguy/api-design-first-with-swagger)

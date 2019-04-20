Exercise 3: Create a Weather service
===========
You will see how easy it is to build RESTful Web services using Spring Web MVC and Spring Test MVC test-driven. The task of this exercise is to implement an endpoint `/api/weather/now/{myCountry}/{myCity}` as specified in the table:

| HTTP Verb   |  CRUD      | Media type   | HTTP Response Body | HTTP Status Code) | 
| ----------- | ---------- | ------------ | ----------- | --------------------------------------- |
| GET         | Read       | JSON         |  { "name": "myCity", "temperature": 280.0 } | 200 (OK)    | 


## Step 1: Create JUnit Service level Tests
In Eclipse within the (source) folder named `src/test/java` create an `WeatherControllerTest` class in the package `com.sap.earlytalent.controllers` and copy the code from here:

```java
import static org.springframework.http.MediaType.*;
import static org.hamcrest.Matchers.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@RunWith(SpringRunner.class)
@SpringBootTest
@AutoConfigureMockMvc
public class WeatherControllerTest {

    private static final String SOME_COUNTRY = "Germany";
    private static final String SOME_CITY = "Sinsheim";
    
    @Autowired
    private MockMvc mockMvc;
    
    @Test
    public void getWeather() throws Exception {
        mockMvc.perform(buildGetNowRequest(SOME_COUNTRY, SOME_CITY))
                .andExpect(status().isOk())
                .andExpect(content().contentType(APPLICATION_JSON_UTF8))
                .andExpect(jsonPath("$.name", is("Sinsheim")))
                .andExpect(jsonPath("$.temperature", is(280.0)));
    }

    private MockHttpServletRequestBuilder buildGetNowRequest(String country, String city) throws Exception {
        return get("/api/weather/now/" + country + "/" + city);
    }
}
```
- Make use of the `CTRL+SHIFT+O` shortcut to organize your missing imports.

#### Run JUnit Tests in Eclipse
As described here: [Exercise 1: Getting Started](https://github.com/ccjavadev/cc-coursematerial/blob/master/SpringBoot/Exercise_1_SpringBoot_GettingStarted.md#step-7-run-junit-tests-in-eclipse). The JUnit test fail as desired, because the endpoint isn't implemented; it should be fixed by end of this exercise.

## Step 2: Define and implement new REST endpoints
Now we want to satisfy the failing JUnit test by implementing the service endpoints as specified in the table above.

- Create an `Weather` class in the package `com.sap.earlytalent.models` with the properties `name` (String) and `temperature` (double). **Note that the JSON converter requires setters and getters for private fields and a default constructor!**

- Create a `WeatherController` class in the package `com.sap.earlytalent.controllers`:
```java
@RestController
@RequestMapping(WeatherController.PATH)
public class WeatherController {
    public static final String PATH = "/api/weather";

    @RequestMapping("/now/{country}/{city}")
    public Weather getWeather(@PathVariable String country, @PathVariable String city) {
        // return this.weatherService.getWeather(country, city);
        Weather weather = new Weather();
        weather.setName(city);
        weather.setTemperature(280.0);
        return weather;
    }
}
```
- Make use of the `CTRL+SHIFT+O` shortcut to organize your missing imports.

#### Run the Microservice locally
As described here: [Exercise 1: Getting Started](https://github.com/ccjavadev/cc-coursematerial/blob/master/SpringBoot/Exercise_1_SpringBoot_GettingStarted.md#step-3-run-microservice-in-eclipse)

#### Test your endpoint manually
Test the REST Service `http://localhost:8080/api/weather/now/Germany/Sinsheim` manually in the Browser or `Postman` chrome plugin.

When calling the `/mappings` REST endpoint you can expect that the new endpoint `/api/weather/now/{country}/{city}` is listed as well.

#### Run JUnit Tests in Eclipse
Finally execute your JUnit tests again. If you see a green bar, your tests have run successful. 


***
<dl>
  <dd>
  <div class="footer">&copy; 2018 SAP SE</div>
  </dd>
</dl>
<hr>
<a href="Exercise_2_SpringBoot_DeployAdsOnCloudFoundry.md">
  <img align="left" alt="Previous Exercise">
</a>
<a href="Exercise_4_CallExternalWeatherService.md">
  <img align="right" alt="Next Exercise">
</a>



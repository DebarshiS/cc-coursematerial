Exercise 4: Connect to external Service
==========================================
As of now we have hard-coded the temperature. Here you can learn how to call synchronously an external Weather service to get the current temperature for "any" City in the World. The service is provided by https://openweathermap.org. Furthermore we have to ensure that our JUnit test will never call the external service, as the calls (per minute) are limited / not free of charge.

#### Explore external service
Before we start with the implementation we want to get familiar with the external Weather service.
You can test the following HTTP service manually in the browser or using `Postman` Chrome plugin:
http://api.openweathermap.org/data/2.5/weather?q=Sinsheim,Germany&APPID=4a7dc30e87b625da187ba9b39758dcb7. This returns the current weather information for the city `Sinsheim`. Note that the `temperature` is part of the "main" JSON property. Note also that the `APPID` is a personal one! You can get your own `APPID`, when you register yourself at [openweathermap.org](https://openweathermap.org). For this Exercise you can make use of it.

## Step 1: Call external Weather service via HTTP
Create a new class `WeatherService` in package `com.sap.earlytalent.services` and copy the code from here:
```java
@Component
public class WeatherService {
    private RestTemplate restTemplate;

    private static final String WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={city},{country}&APPID={key}";

    @Value("${WEATHER_SERVICE_KEY}") //reads value from system environment
    private String weatherServiceAppID;

    @Autowired
    public WeatherService(RestTemplateBuilder restTemplateBuilder) {
        this.restTemplate = restTemplateBuilder.build();
    }

    public Weather getCurrentWeather(String country, String city) {
        URI url = new UriTemplate(WEATHER_URL).expand(city, country, weatherServiceAppID);
        return invoke(url, Weather.class);
    }

    private <T> T invoke(URI url, Class<T> responseType) {
        RequestEntity<?> request = RequestEntity.get(url).accept(MediaType.APPLICATION_JSON).build();

        ResponseEntity<T> exchange = this.restTemplate.exchange(request, responseType);

        return exchange.getBody();
    }
}
```

## Step 2: Integrate `WeatherService` into `WeatherController`
Instead of returning fake data in the `WeatherController`, we want to call the `getCurrentWeather()` method of the `WeatherService`.

- In order to get the `WeatherService` bean injected into the `WeatherController`, we are going to declare the following Constructor and private field:
```java
private final WeatherService weatherService; 

@Autowired
public WeatherController(WeatherService weatherService) { 
    this.weatherService  = weatherService;
}
```
- Replace the implementation of the `WeatherController.getWeather()` method in such a way, that the `weatherService.getCurrentWeather` gets executed.

## Step 3: Run in Eclipse IDE
Before you (re-)start your Java Application within Eclipse, you need to adapt the Run Configuration. To do so right-click the `weather` project in the `Project Explorer` and select `Run As` -> `Run Configurations...`. 

In the `Run Configurations` dialog ensure that the `Java Application` - `WeatherApplication` is selected.
- switch to the `Environment` tab and add the following environment variable:
  - name: `WEATHER_SERVICE_KEY`
  - value: `4a7dc30e87b625da187ba9b39758dcb7`
- switch to the `Arguments` tab and add the proxy settings to the VM arguments:
  - ` -Dhttp.proxyHost=proxy.wdf.sap.corp -Dhttp.proxyPort=8080`

**Why are proxy settings required?** If you run your service locally within the SAP corporate network, the host `api.openweathermap.org` cannot be resolved. If you apply the proxy settings to the Java process (via VM arguments) then the SAP proxy is used which is able to resolve the host name. 

#### [Alternative Option] Run on the Command Line
Ensure that you are in the project root e.g. ~/workspace/weather.
Linux:
```
export WEATHER_SERVICE_KEY=4a7dc30e87b625da187ba9b39758dcb7
mvn spring-boot:run -Dhttp.proxyHost=proxy.wdf.sap.corp -Dhttp.proxyPort=8080
```

#### Test your endpoint manually
Test the REST Service [`http://localhost:8080/api/weather/now/Germany/Sinsheim`](http://localhost:8080/api/weather/now/Germany/Sinsheim) manually in the Browser or `Postman` chrome plugin. Note, that it returns right now `"temperature":0.0`. Right? This is because the JSON Mapping needs to be adapted slightly. We are going to fix that, test-driven in the following step.

## Step 4: Adapt JUnit tests to avoid call to external service 
In our component test we want to test our microservice without calling the external Weather service. That's why we have to provide some mocking.

- Create a source folder `src/test/resources` and create there a file with name `WeatherDEGermany.json` and copy the code from [here](https://github.wdf.sap.corp/raw/D048418/cc-weather-spring-boot/master/src/test/resources/WeatherDEGermany.json).

- In the `WeatherControllerTest` class we want to return the content of the JSON file instead of doing the real call. Therefore we have to mock the `weatherService.getCurrentWeather()` method. We are doing that by adding the following fields and `setup` method into our Test class:
```java
@Autowired
private ObjectMapper objectMapper; 

@MockBean
private WeatherService weatherService; 

@Before
public void setup() throws Exception {
    File file = ResourceUtils.getFile(this.getClass().getResource("/WeatherDEGermany.json"));
    Weather weather = objectMapper.readValue(file, Weather.class);
    Mockito.when(weatherService.getCurrentWeather(Mockito.anyString(), Mockito.anyString())).thenReturn(weather);
}
```
####  Run JUnit Tests in Eclipse
As described here: [Exercise 1: Getting Started](https://github.com/ccjavadev/cc-coursematerial/blob/master/SpringBoot/Exercise_1_SpringBoot_GettingStarted.md#step-7-run-junit-tests-in-eclipse). The JUnit test fail as desired, because the JSON Mapping isn't implemented; we have to map "main-temp" to "temperature". 

#### Implement JSON Mapping 
Within your `Weather` class add the following method, which gets called by the JSON Parser for the property "main":
```java
@JsonProperty("main")
public void setMain(Map<String, Object> main) {
    setTemperature(Double.parseDouble(main.get("temp").toString()));
}
```

Finally execute your JUnit tests again. If you see a green bar, you are done.

#### Test your endpoint manually
Test the REST Service [`http://localhost:8080/api/weather/now/Germany/Sinsheim`](http://localhost:8080/api/weather/now/Germany/Sinsheim) manually in the Browser or `Postman` chrome plugin. Enter also other city names...

## Step 5: Push and run in CF
Before pushing the application to Cloud Foundry  as described in [Exercise 2: Deploy Microservice on CF](https://github.com/ccjavadev/cc-coursematerial/blob/master/SpringBoot/Exercise_2_SpringBoot_DeployAdsOnCloudFoundry.md#step-3-push-your-service), the `WEATHER_SERVICE_KEY` needs to be configured as a system environment variable. This can easily be done in the `manifest.yml` file by adding another entry under `env`:
```
env:
    WEATHER_SERVICE_KEY: '4a7dc30e87b625da187ba9b39758dcb7'
```

***
<dl>
  <dd>
  <div class="footer">&copy; 2018 SAP SE</div>
  </dd>
</dl>
<hr>
<a href="Exercise_3_SpringBoot_CreateWeatherService.md">
  <img align="left" alt="Previous Exercise">
</a>

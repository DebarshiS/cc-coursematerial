# Test Strategy - Additional Information

## Performance Testing - JMeter
 - [Short introduction video to JMeter](https://video.sap.com/media/t/1_4nj2lh3u/39197781)

## Performance Testing - Maximum (response time) over averages or percentiles
There are multiple reasons why measuring (and asserting) averages or percentiles of latencies is not enough: 
- Most websites use a large number of requests per site. Therefore, with high probability, most users also experience the worst case scenario on a single request. This single slow request could determine the duration of the whole call.
- JMeter (and most other such tools) measures performance by running multiple requests one after another in each thread. Imagine the scenario of a hickup, that is, all requests in a timeframe getting delayed until the end of this timeframe, due to some performance issue. Then, JMeter will only yield a single bad measurement influenced by this hickup per thread. Most likely, this single measurement might not meaningfully influence the average or be incorporated into the percentile measurement at all. 
- [Gil Tene - How NOT to Measure Latency](https://www.youtube.com/watch?v=lJ8ydIuPFeU) 

## Test Quiz / Contract Tests
The last question of the quiz with the answer "???" is intended to hint at Contract / Consumer-Driven tests.
As mentioned above the quiz, the tests should be designed from the perspective of the Advertisement microservice.
As such, to test if the User microservice behaves correctly, the mentioned test should be added to the User service's code base, using the idea of Consumer-Driven tests.

## Further Reading
- [ThoughtWorks "Article" about Testing Microservices](http://martinfowler.com/articles/microservice-testing])
- [SAP ASE Wiki - Agile Test Automation Strategy](https://wiki.wdf.sap.corp/wiki/display/ASE/Agile+Test+Automation+Strategy)

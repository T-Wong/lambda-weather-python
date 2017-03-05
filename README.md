# Lambda Weather Python
AWS Lambda function that gets weather data from [OpenWeatherMap](https://openweathermap.org/) and sends it an [InitialState](https://www.initialstate.com/) dashboard.

## Secrets
The OpenWeatherMap API key, InitialState bucket key, and InitialState access key are all stored in a private HashiCorp Vault instance. Lambda is able to decrypt these secrets with a Vault token. The Vault token is encrypted using KMS and then decrypted at runtime.

## Weather
The `get_weather.py` file in the root directory is where the Lambda function. All of the other directories are dependencies. Right now, it is only configured to get weather data from `Bothell, US`, but this Lambda function can be modified to accept any location.

## License & Authors
- Author:: Tyler Wong ([ty-w@live.com](mailto:ty-w@live.com))

```text
Copyright 2017, Tyler Wong

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.```

## HA Custom Analytics

This webpage contains some of the latest Home Assistant Analytics data

The automated data collection in this repository is done each 6 hours.

Please refer to the [README](https://github.com/Vaskivskyi/ha-custom-analytics) for the detailed info.

## Usage

#### Historical Data

The repository now includes historical time series data for each custom integration showing how installation counts changed over time. This data is automatically generated from the raw daily snapshots and is available at:

```
https://vaskivskyi.github.io/ha-custom-analytics/history/INTEGRATION_NAME/total.json

https://vaskivskyi.github.io/ha-custom-analytics/history/INTEGRATION_NAME/version-VERSION.json
```

Each file contains a JSON object with date:count mappings, for example:
```json
{
  "2022-10-26": 1000,
  "2022-10-27": 1050,
  "2022-10-28": 1100
}
```

This data can be used to plot popularity trends and observe the adoption of different integration versions over time.

#### Shields.io badges

You can use these generated files in the following way (or check the [official Shields documentation](https://shields.io/endpoint)):

```
https://img.shields.io/endpoint?url=YOUR_ENDPOINT
```

If you would like to use already generated data, use the following endpoints:

```
https://vaskivskyi.github.io/ha-custom-analytics/badges/INTEGRATION_NAME/total.json

https://vaskivskyi.github.io/ha-custom-analytics/badges/INTEGRATION_NAME/version-VERSION.json
```

Example for a badge of my `asusrouter` integration:

```
https://img.shields.io/endpoint?url=https://vaskivskyi.github.io/ha-custom-analytics/badges/asusrouter/total.json
```

![AsusRouter installations](https://img.shields.io/endpoint?url=https://vaskivskyi.github.io/ha-custom-analytics/badges/asusrouter/total.json)

All the styles are available as for any other Shields badges.

![AsusRouter installations](https://img.shields.io/endpoint?url=https://vaskivskyi.github.io/ha-custom-analytics/badges/asusrouter/total.json&style=for-the-badge&color=yellow&labelColor=blue)

## Support

If you like the idea of custom HA analytics, you can support me by buying me a coffee.

<a href="https://www.buymeacoffee.com/vaskivskyi" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" style="height: 60px !important;"></a>

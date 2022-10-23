## HA Custom Analytics

This repository contains scripts to get the latest Home Assistant Analytics data and process it. The latest data is also available in the `docs` folder.

The automated data collection in this repository is done each 6 hours.

## Usage

#### Shields.io badges

Python script `custom_integration_badges.py` is used to generate JSON files compatible with Shields badges, showing the number of active installations of custom integrations.

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

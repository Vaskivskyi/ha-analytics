import aiohttp
import asyncio
import json
import os
from typing import Any

DATA_URL = "https://analytics.home-assistant.io/custom_integrations.json"
PROCESSED_PATH = "docs/badges/"


async def async_get_data(session: aiohttp.ClientSession | None = None):
    """Load data"""

    _session = session if session is not None else aiohttp.ClientSession()

    async with _session.get(
        url=DATA_URL,
    ) as r:
        json_body = await r.json()

    _session.close()

    return json_body


def generate_badge(installations: int) -> dict[str, Any]:
    """Generate badge"""

    return {
        "schemaVersion": 1,
        "label": "Installations",
        "message": f"{installations}",
    }


async def async_test():
    data = await async_get_data()

    for integration in data:
        path = PROCESSED_PATH + integration
        # Check the path
        if not os.path.exists(path):
            os.makedirs(path)

        # Generate total badge
        if "total" in data[integration]:
            badge = generate_badge(data[integration]["total"])
            with open(f"{path}/total.json", "w") as file:
                json.dump(badge, file)
        # Generate per-version badges
        if "versions" in data[integration]:
            for version in data[integration]["versions"]:
                badge = generate_badge(data[integration]["versions"][version])
                with open(f"{path}/version-{version}.json", "w") as file:
                    json.dump(badge, file)


loop = asyncio.get_event_loop()
loop.run_until_complete(async_test())
loop.close()

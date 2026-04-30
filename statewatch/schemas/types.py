from typing import TypedDict


AssetMetadata = TypedDict(
    "AssetMetadata",
    {
        "1. Information": str,
        "2. Digital Currency Code": str,
        "3. Digital Currency Name": str,
        "4. Market Code": str,
        "5. Market Name": str,
        "6. Last Refreshed": str,
        "7. Time Zone": str,
    },
)

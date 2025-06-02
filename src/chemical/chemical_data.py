# src/chemical/chemical_data.py

CHEMICAL_DATA = {
    "categories": [
        "metal",
        "nonmetal",
        "metalloid",
        "transition metal",
        "lanthanide",
        "actinide",
        "noble gas",
        "alkali metal",
        "alkaline earth metal",
        "post-transition metal",
        "metalloid",
        "halogen"
    ],
    "groups": [
        {
            "id": 1,
            "name": "alkali metals"
        },
        {
            "id": 2,
            "name": "alkaline earth metals"
        },
        {
            "id": 3,
            "name": "scandium family"
        },
        {
            "id": 4,
            "name": "titanium family"
        },
        {
            "id": 5,
            "name": "vanadium family"
        },
        {
            "id": 6,
            "name": "chromium family"
        },
        {
            "id": 7,
            "name": "manganese family"
        },
        {
            "id": 8,
            "name": "iron family"
        },
        {
            "id": 9,
            "name": "cobalt family"
        },
        {
            "id": 10,
            "name": "nickel family"
        },
        {
            "id": 11,
            "name": "copper family"
        },
        {
            "id": 12,
            "name": "zinc family"
        },
        {
            "id": 13,
            "name": "boron family"
        },
        {
            "id": 14,
            "name": "carbon family"
        },
        {
            "id": 15,
            "name": "nitrogen family"
        },
        {
            "id": 16,
            "name": "chalcogens"
        },
        {
            "id": 17,
            "name": "halogens"
        },
        {
            "id": 18,
            "name": "noble gases"
        }
    ]
}

CATEGORY_NAMES: list[str] = CHEMICAL_DATA["categories"]
GROUP_NAMES: list[str] = [group["name"] for group in CHEMICAL_DATA["groups"]]
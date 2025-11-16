from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_components():
    """
    Get a list of available components for the library.
    """
    # In a real application, this would come from a database.
    # For Cycle 2, we'll use a hardcoded list.
    components = [
        {
            "id": "jst-xh-2p",
            "type": "connector",
            "name": "JST XH-2P",
            "data": {
                "manufacturer": "JST",
                "part_number": "XH-2P",
                "pins": [{"id": "1"}, {"id": "2"}],
            },
        },
        {
            "id": "jst-xh-3p",
            "type": "connector",
            "name": "JST XH-3P",
            "data": {
                "manufacturer": "JST",
                "part_number": "XH-3P",
                "pins": [{"id": "1"}, {"id": "2"}, {"id": "3"}],
            },
        },
        {
            "id": "molex-kk-2p",
            "type": "connector",
            "name": "Molex KK-2P",
            "data": {
                "manufacturer": "Molex",
                "part_number": "22-01-3027",
                "pins": [{"id": "1"}, {"id": "2"}],
            },
        },
        {
            "id": "wire-red-22awg",
            "type": "wire",
            "name": "22 AWG Red",
            "data": {
                "manufacturer": "Generic",
                "part_number": "UL1007-22-RED",
                "color": "red",
                "gauge": 22,
            },
        },
        {
            "id": "wire-black-22awg",
            "type": "wire",
            "name": "22 AWG Black",
            "data": {
                "manufacturer": "Generic",
                "part_number": "UL1007-22-BLK",
                "color": "black",
                "gauge": 22,
            },
        },
    ]
    return components

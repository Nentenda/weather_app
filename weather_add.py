import asyncio
import winsdk.windows.devices.geolocation as wdg


async def getcoords():
    locator = wdg.Geolocator()
    pos = await locator.get_geoposition_async()
    return [f"accuracy: {pos.coordinate.accuracy},"
            f"longitude: {pos.coordinate.longitude},"
            f"latitude: {pos.coordinate.latitude}"]

def getloc():
    try:
        return asyncio.run(getcoords())
    except PermissionError:
        print("ERROR: You need to allow applications to access you location in Windows settings")


print(*getloc())

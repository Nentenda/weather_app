from dataclasses import dataclass
from subprocess import Popen, PIPE
from typing import Literal
import config
from exceptions import CantGetCoordinates


@dataclass(slots=True, frozen=True)
class Coordinates:
    latitude: float
    longitude: float


def get_gps_coordinates() -> Coordinates:
    """Returns gps coordinates using Windows GPS"""
    coordinates = _get_weather_add_coordinates()
    return _round_coordinates(coordinates)


def _get_weather_add_coordinates() -> Coordinates:
    weather_add_output = _get_weather_add_output()
    coordinates = _parse_coordinates(weather_add_output)
    return coordinates


def _get_weather_add_output() -> bytes:
    procces = Popen(["weather_add.py"], stdout=PIPE, shell=True)
    output, err = procces.communicate()
    exit_code = procces.wait()
    if err is not None or exit_code != 0:
        raise CantGetCoordinates
    return output


def _parse_coordinates(weather_add_output: bytes) -> Coordinates:
    output = weather_add_output.decode().strip().lower().split(",")
    return Coordinates(
        latitude=_parse_coord(output, "latitude"),
        longitude=_parse_coord(output, "longitude")
    )


def _parse_coord(
        output: list[str],
        coord_type: Literal["latitude"] | Literal["longitude"]) -> float:
    for line in output:
        if line.startswith(f"{coord_type}:"):
            return _parse_float_coordinate(line.split(":")[1])


def _parse_float_coordinate(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        raise CantGetCoordinates


def _round_coordinates(coordinates: Coordinates) -> Coordinates:
    if not config.USE_ROUNDED_COORDS:
        return coordinates
    return Coordinates(*map(lambda c: round(c, 1), [coordinates.latitude,
                                                    coordinates.longitude]
                            ))


if __name__ == "__main__":
    print(get_gps_coordinates())

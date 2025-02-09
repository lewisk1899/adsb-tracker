from pydantic import BaseModel, root_validator
from typing import List, Optional

class StateVector(BaseModel):
    icao24: str
    callsign: Optional[str]
    origin_country: str
    time_position: Optional[int]
    last_contact: int
    longitude: Optional[float]
    latitude: Optional[float]
    baro_altitude: Optional[float]
    on_ground: bool
    velocity: Optional[float]
    true_track: Optional[float]
    vertical_rate: Optional[float]
    sensors: Optional[List[int]]
    geo_altitude: Optional[float]
    squawk: Optional[str]
    spi: bool
    position_source: int

    @classmethod
    def from_list(cls, data: List):
        return cls(
            icao24=data[0], callsign=data[1], origin_country=data[2], time_position=data[3],
            last_contact=data[4], longitude=data[5], latitude=data[6], baro_altitude=data[7],
            on_ground=data[8], velocity=data[9], true_track=data[10], vertical_rate=data[11],
            sensors=data[12], geo_altitude=data[13], squawk=data[14], spi=data[15], position_source=data[16]
        )

class States(BaseModel):
    time: int
    states: List[StateVector]

    @root_validator(pre=True)
    def parse_states(cls, values):
        if "states" in values and isinstance(values["states"], list):
            values["states"] = [StateVector.from_list(state) for state in values["states"]]
        return values


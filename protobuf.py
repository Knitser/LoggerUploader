import protobuf3


class OBDParameters(protobuf3.Message):
    number_of_dtc = protobuf3.StringField(field_number=1)
    engine_load = protobuf3.StringField(field_number=2)
    coolant_temperature = protobuf3.StringField(field_number=3)
    fuel_pressure = protobuf3.StringField(field_number=4)
    engine_rpm = protobuf3.StringField(field_number=5)
    vehicle_speed = protobuf3.StringField(field_number=6)
    throttle_position = protobuf3.StringField(field_number=7)
    fuel_level = protobuf3.StringField(field_number=8)
    ambient_air_temperature = protobuf3.StringField(field_number=9)
    fuel_type = protobuf3.StringField(field_number=10)
    engine_oil_temperature = protobuf3.StringField(field_number=11)
    fuel_rate = protobuf3.StringField(field_number=12)
    fault_codes = protobuf3.StringField(field_number=13)
    vin = protobuf3.StringField(field_number=14)

import usb_hid
import neopixel
from adafruit_hid import find_device

LAMP_NOT_PROGRAMMABLE = 0x00
LAMP_IS_PROGRAMMABLE = 0x01

LAMP_ARRAY_ATTRIBUTES_REPORT_ID = 1
LAMP_ATTRIBUTES_REQUEST_REPORT_ID = 2
LAMP_ATTRIBUTES_RESPONSE_REPORT_ID = 3
LAMP_MULTI_UPDATE_REPORT_ID = 4
LAMP_RANGE_UPDATE_REPORT_ID = 5
LAMP_ARRAY_CONTROL_REPORT_ID = 6

class LampArrayAttributesReport:
    def __init__(self, report_id, lamp_count, bounding_box_width_mm, bounding_box_height_mm, bounding_box_depth_mm, lamp_array_kind, min_update_interval_us):
        self.report_id = report_id
        self.lamp_count = lamp_count
        self.bounding_box_width_mm = bounding_box_width_mm
        self.bounding_box_height_mm = bounding_box_height_mm
        self.bounding_box_depth_mm = bounding_box_depth_mm
        self.lamp_array_kind = lamp_array_kind
        self.min_update_interval_us = min_update_interval_us

class LampAttributesRequestReport:
    def __init__(self, report_id, lamp_id):
        self.report_id = report_id
        self.lamp_id = lamp_id

class LampAttributesResponseReport:
    def __init__(self, report_id, attributes):
        self.report_id = report_id
        self.attributes = attributes

class LampMultiUpdateReport:
    def __init__(self, report_id, lamp_count, lamp_update_flags, lamp_ids, update_colors):
        self.report_id = report_id
        self.lamp_count = lamp_count
        self.lamp_update_flags = lamp_update_flags
        self.lamp_ids = lamp_ids
        self.update_colors = update_colors

class LampRangeUpdateReport:
    def __init__(self, report_id, lamp_update_flags, lamp_id_start, lamp_id_end, update_color):
        self.report_id = report_id
        self.lamp_update_flags = lamp_update_flags
        self.lamp_id_start = lamp_id_start
        self.lamp_id_end = lamp_id_end
        self.update_color = update_color

class LampArrayControlReport:
    def __init__(self, report_id, autonomous_mode):
        self.report_id = report_id
        self.autonomous_mode = autonomous_mode

class LampPurposeKind:
    LampPurposeControl = 1
    LampPurposeAccent = 2
    LampPurposeBranding = 4
    LampPurposeStatus = 8
    LampPurposeIllumination = 16
    LampPurposePresentation = 32

class LampArrayKind:
    LampArrayKindKeyboard = 1
    LampArrayKindMouse = 2
    LampArrayKindGameController = 3
    LampArrayKindPeripheral = 4
    LampArrayKindScene = 5
    LampArrayKindNotification = 6
    LampArrayKindChassis = 7
    LampArrayKindWearable = 8
    LampArrayKindFurniture = 9
    LampArrayKindArt = 10

class LampArrayColor:
    __slots__ = ['red_channel', 'green_channel', 'blue_channel', 'intensity_channel']

    def __init__(self, red_channel, green_channel, blue_channel, intensity_channel):
        self.red_channel = red_channel
        self.green_channel = green_channel
        self.blue_channel = blue_channel
        self.intensity_channel = intensity_channel

class LampAttributes:
    __slots__ = [
        'lamp_id', 'position_x_mm', 'position_y_mm', 'position_z_mm',
        'update_latency_ms', 'lamp_purposes', 'red_level_count', 'green_level_count',
        'blue_level_count', 'intensity_level_count', 'is_programmable', 'lamp_key'
    ]

    def __init__(
        self, lamp_id, position_x_mm, position_y_mm, position_z_mm,
        update_latency_ms, lamp_purposes, red_level_count, green_level_count,
        blue_level_count, intensity_level_count, is_programmable, lamp_key
    ):
        self.lamp_id = lamp_id
        self.position_x_mm = position_x_mm
        self.position_y_mm = position_y_mm
        self.position_z_mm = position_z_mm
        self.update_latency_ms = update_latency_ms
        self.lamp_purposes = lamp_purposes
        self.red_level_count = red_level_count
        self.green_level_count = green_level_count
        self.blue_level_count = blue_level_count
        self.intensity_level_count = intensity_level_count
        self.is_programmable = is_programmable
        self.lamp_key = lamp_key

LAMP_UPDATE_FLAG_UPDATE_COMPLETE = 1

def milliseconds_to_microseconds(x):
    return x * 1000

def millimeters_to_micrometers(x):
    return x * 1000

class MicrosoftHidLampArray:
    def __init__(self, device, lamp_count, bounding_box_width_mm, bounding_box_height_mm, bounding_box_depth_mm, kind, min_update_interval_ms):
        self._lamparray_device = find_device(device, usage_page=0x59, usage=0x01, timeout=5)
        
        if lamp_count > 65535:
            raise ValueError("lamp_count exceeds the maximum allowed value of 65535")

        self.lamp_count = lamp_count
        self.bounding_box_width_mm = bounding_box_width_mm
        self.bounding_box_height_mm = bounding_box_height_mm
        self.bounding_box_depth_mm = bounding_box_depth_mm
        self.kind = kind
        self.min_update_interval_ms = min_update_interval_ms

        # Generate default lamp attributes
        self.lamp_attributes = self.generate_default_lamp_attributes()

        self.state_size = self.lamp_count
        self.cached_state_write_to = [LampArrayColor(0, 0, 0, 0) for _ in range(self.lamp_count)]
        self.cached_state_read_from = [LampArrayColor(0, 0, 0, 0) for _ in range(self.lamp_count)]
        self.is_autonomous_mode = True
        self.last_lamp_id_requested = 0

        # Debug print
        print(f"Lamp array initialized with {self.lamp_count} lamps.")

    def generate_default_lamp_attributes(self):
        # Generate default lamp attributes based on positions and other parameters
        attributes = []
        for i in range(self.lamp_count):
            x_position = (i % 8) * 15  # Example: placing lamps in a grid with 15mm spacing
            y_position = (i // 8) * 15
            attributes.append(
                LampAttributes(
                    lamp_id=i,
                    position_x_mm=x_position,
                    position_y_mm=y_position,
                    position_z_mm=0,
                    update_latency_ms=self.min_update_interval_ms,
                    lamp_purposes=LampPurposeKind.LampPurposeAccent,
                    red_level_count=0xFF,
                    green_level_count=0xFF,
                    blue_level_count=0xFF,
                    intensity_level_count=0x01,
                    is_programmable=LAMP_IS_PROGRAMMABLE,
                    lamp_key=0
                )
            )
        return attributes

    def get_current_state(self, current_state):
        if not isinstance(current_state, list) or len(current_state) != self.lamp_count:
            raise ValueError("current_state must be a list with the same size as lamp_count")

        if self.is_autonomous_mode:
            for i in range(len(current_state)):
                current_state[i] = LampArrayColor(0, 0, 0, 0)
        else:
            for i in range(len(current_state)):
                current_state[i] = self.cached_state_read_from[i]

        return self.is_autonomous_mode

    @property
    def received_get_feature_report(self):
        raise NotImplementedError

    @received_get_feature_report.setter
    def received_get_feature_report(self, report_id):
        try:
            if report_id == LAMP_ARRAY_ATTRIBUTES_REPORT_ID:
                self.send_lamp_array_attributes_report()
            elif report_id == LAMP_ATTRIBUTES_RESPONSE_REPORT_ID:
                self.send_lamp_attributes_report()
        except Exception as e:
            raise RuntimeError(f"Error processing get feature report: {e}")

    @property
    def received_set_feature_report(self):
        raise NotImplementedError

    @received_set_feature_report.setter
    def received_set_feature_report(self, report):
        report_id, data, length = report
        try:
            if report_id == LAMP_ATTRIBUTES_REQUEST_REPORT_ID:
                self.update_request_lamp_from_lamp_attributes_request_report(data, length)
            elif report_id == LAMP_MULTI_UPDATE_REPORT_ID:
                self.update_lamp_state_cache_from_multi_update_report(data, length)
            elif report_id == LAMP_RANGE_UPDATE_REPORT_ID:
                self.update_lamp_state_cache_from_range_update_report(data, length)
            elif report_id == LAMP_ARRAY_CONTROL_REPORT_ID:
                self.process_control_report(data, length)
        except Exception as e:
            raise RuntimeError(f"Error processing set feature report: {e}")

    def send_feature_report(self, report):
        # Add implementation for sending the feature report
        pass

    @property
    def send_lamp_array_attributes_report(self):
        try:
            lamp_array_attributes_report = {
                'report_id': LAMP_ARRAY_ATTRIBUTES_REPORT_ID,
                'lamp_count': self.lamp_count,
                'bounding_box_width_um': millimeters_to_micrometers(self.bounding_box_width_mm),
                'bounding_box_height_um': millimeters_to_micrometers(self.bounding_box_height_mm),
                'bounding_box_depth_um': millimeters_to_micrometers(self.bounding_box_depth_mm),
                'kind': self.kind,
                'min_update_interval_us': milliseconds_to_microseconds(self.min_update_interval_ms)
            }
            self.send_feature_report(lamp_array_attributes_report)
        except Exception as e:
            raise RuntimeError(f"Error sending lamp array attributes report: {e}")

    @property
    def send_lamp_attributes_report(self):
        try:
            if self.last_lamp_id_requested >= self.lamp_count:
                self.last_lamp_id_requested = 0

            lamp_attributes = self.lamp_attributes[self.last_lamp_id_requested]

            lamp_attribute_report = {
                'report_id': LAMP_ATTRIBUTES_RESPONSE_REPORT_ID,
                'attributes': {
                    'lamp_id': lamp_attributes.lamp_id,
                    'position_x_um': millimeters_to_micrometers(lamp_attributes.position_x_mm),
                    'position_y_um': millimeters_to_micrometers(lamp_attributes.position_y_mm),
                    'position_z_um': millimeters_to_micrometers(lamp_attributes.position_z_mm),
                    'update_latency_us': milliseconds_to_microseconds(lamp_attributes.update_latency_ms),
                    'lamp_purposes': lamp_attributes.lamp_purposes,
                    'red_level_count': lamp_attributes.red_level_count,
                    'green_level_count': lamp_attributes.green_level_count,
                    'blue_level_count': lamp_attributes.blue_level_count,
                    'intensity_level_count': lamp_attributes.intensity_level_count,
                    'is_programmable': lamp_attributes.is_programmable,
                    'lamp_key': lamp_attributes.lamp_key
                }
            }
            self.send_feature_report(lamp_attribute_report)
            self.last_lamp_id_requested += 1
        except Exception as e:
            raise RuntimeError(f"Error sending lamp attributes report: {e}")

    @property
    def update_request_lamp_from_lamp_attributes_request_report(self):
        raise NotImplementedError

    @update_request_lamp_from_lamp_attributes_request_report.setter
    def update_request_lamp_from_lamp_attributes_request_report(self, report):
        try:
            report_id, data, length = report

            if report_id != LAMP_ATTRIBUTES_REQUEST_REPORT_ID:
                raise ValueError("Invalid report ID")

            if length < len(data):
                raise ValueError("Data length mismatch")

            lamp_id = int.from_bytes(data[:2], 'little')  # Assuming LampId is 2 bytes
            if lamp_id < self.lamp_count:
                self.last_lamp_id_requested = lamp_id
            else:
                self.last_lamp_id_requested = 0
        except Exception as e:
            raise RuntimeError(f"Error updating request lamp from lamp attributes request report: {e}")

    @property
    def update_lamp_state_cache_from_multi_update_report(self):
        raise NotImplementedError

    @update_lamp_state_cache_from_multi_update_report.setter
    def update_lamp_state_cache_from_multi_update_report(self, report):
        try:
            report_id, data, length = report

            if report_id != LAMP_MULTI_UPDATE_REPORT_ID:
                raise ValueError("Invalid report ID")

            lamp_count = data[1]  # Assuming LampCount is at index 1
            lamp_ids = data[2:2+lamp_count]  # Assuming LampIds start at index 2
            update_colors_start = 2 + lamp_count
            update_colors = data[update_colors_start:update_colors_start + lamp_count*4]  # Assuming each LampArrayColor is 4 bytes

            for i in range(lamp_count):
                lamp_id = lamp_ids[i]
                if lamp_id < self.lamp_count:
                    color_data = update_colors[i*4:(i+1)*4]
                    self.cached_state_write_to[lamp_id] = LampArrayColor(*color_data)

            # Check if the update is complete
            lamp_update_flags = data[-1]  # Assuming flags are at the last byte
            if lamp_update_flags & LAMP_UPDATE_FLAG_UPDATE_COMPLETE:
                self.cached_state_read_from = self.cached_state_write_to.copy()
        except Exception as e:
            raise RuntimeError(f"Error updating lamp state cache from multi update report: {e}")

    @property
    def update_lamp_state_cache_from_range_update_report(self):
        raise NotImplementedError

    @update_lamp_state_cache_from_range_update_report.setter
    def update_lamp_state_cache_from_range_update_report(self, report):
        try:
            report_id, data, length = report

            if report_id != LAMP_RANGE_UPDATE_REPORT_ID:
                raise ValueError("Invalid report ID")

            lamp_id_start = data[1]  # Assuming LampIdStart is at index 1
            lamp_id_end = data[2]  # Assuming LampIdEnd is at index 2
            update_color = LampArrayColor(*data[3:7])  # Assuming UpdateColor is at index 3 and is 4 bytes long
            lamp_update_flags = data[-1]  # Assuming flags are at the last byte

            if lamp_id_start >= 0 and lamp_id_start < self.lamp_count and \
               lamp_id_end >= 0 and lamp_id_end < self.lamp_count and \
               lamp_id_start <= lamp_id_end:

                for i in range(lamp_id_start, lamp_id_end + 1):
                    self.cached_state_write_to[i] = update_color

                if lamp_update_flags & LAMP_UPDATE_FLAG_UPDATE_COMPLETE:
                    self.cached_state_read_from = self.cached_state_write_to.copy()
        except Exception as e:
            raise RuntimeError(f"Error updating lamp state cache from range update report: {e}")

    @property
    def process_control_report(self):
        raise NotImplementedError

    @process_control_report.setter
    def process_control_report(self, report):
        try:
            report_id, data, length = report

            if report_id != LAMP_ARRAY_CONTROL_REPORT_ID:
                raise ValueError("Invalid report ID")

            autonomous_mode = data[1]  # Assuming AutonomousMode is at index 1

            self.is_autonomous_mode = bool(autonomous_mode)
        except Exception as e:
            raise RuntimeError(f"Error processing control report: {e}")

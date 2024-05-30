import usb_hid

HID_LAMPARRAY_REPORT_DESCRIPTOR = bytes((
    0x05, 0x59,                      # Usage Page (Lighting And Illumination)
    0x09, 0x01,                      # Usage (LampArray)
    0xA1, 0x01,                      # Collection (Application)

    # Report ID 1 - LampArrayAttributesReport
    0x85, 0x01,                      # Report ID (1)
    0x09, 0x02,                      # Usage (LampArrayAttributesReport)
    0xA1, 0x02,                      # Collection (Logical)
    0x09, 0x03,                      # Usage (LampCount)
    0x15, 0x00,                      # Logical Minimum (0)
    0x27, 0xFF, 0xFF, 0x00, 0x00,    # Logical Maximum (65535)
    0x75, 0x10,                      # Report Size (16)
    0x95, 0x01,                      # Report Count (1)
    0xB1, 0x03,                      # Feature (Constant, Variable, Absolute)
    0x09, 0x04,                      # Usage (BoundingBoxWidthInMicrometers)
    0x09, 0x05,                      # Usage (BoundingBoxHeightInMicrometers)
    0x09, 0x06,                      # Usage (BoundingBoxDepthInMicrometers)
    0x09, 0x07,                      # Usage (LampArrayKind)
    0x09, 0x08,                      # Usage (MinUpdateIntervalInMicroseconds)
    0x27, 0xFF, 0xFF, 0xFF, 0x7F,    # Logical Maximum (2147483647)
    0x75, 0x20,                      # Report Size (32)
    0x95, 0x05,                      # Report Count (5)
    0xB1, 0x03,                      # Feature (Constant, Variable, Absolute)
    0xC0,                            # End Collection

    # Report ID 2 - LampAttributesRequestReport
    0x85, 0x02,                      # Report ID (2)
    0x09, 0x20,                      # Usage (LampAttributesRequestReport)
    0xA1, 0x02,                      # Collection (Logical)
    0x09, 0x21,                      # Usage (LampId)
    0x27, 0xFF, 0xFF, 0x00, 0x00,    # Logical Maximum (65535)
    0x75, 0x10,                      # Report Size (16)
    0x95, 0x01,                      # Report Count (1)
    0xB1, 0x02,                      # Feature (Data, Variable, Absolute)
    0xC0,                            # End Collection

    # Report ID 3 - LampAttributesResponseReport
    0x85, 0x03,                      # Report ID (3)
    0x09, 0x22,                      # Usage (LampAttributesResponseReport)
    0xA1, 0x02,                      # Collection (Logical)
    0x09, 0x21,                      # Usage (LampId)
    0xB1, 0x02,                      # Feature (Data, Variable, Absolute)
    0x09, 0x23,                      # Usage (PositionXInMicrometers)
    0x09, 0x24,                      # Usage (PositionYInMicrometers)
    0x09, 0x25,                      # Usage (PositionZInMicrometers)
    0x09, 0x27,                      # Usage (UpdateLatencyInMicroseconds)
    0x09, 0x26,                      # Usage (LampPurposes)
    0x27, 0xFF, 0xFF, 0xFF, 0x7F,    # Logical Maximum (2147483647)
    0x75, 0x20,                      # Report Size (32)
    0x95, 0x05,                      # Report Count (5)
    0xB1, 0x02,                      # Feature (Data, Variable, Absolute)
    0x09, 0x28,                      # Usage (RedLevelCount)
    0x09, 0x29,                      # Usage (GreenLevelCount)
    0x09, 0x2A,                      # Usage (BlueLevelCount)
    0x09, 0x2B,                      # Usage (IntensityLevelCount)
    0x09, 0x2C,                      # Usage (IsProgrammable)
    0x09, 0x2D,                      # Usage (InputBinding)
    0x26, 0xFF, 0x00,                # Logical Maximum (255)
    0x75, 0x08,                      # Report Size (8)
    0x95, 0x06,                      # Report Count (6)
    0xB1, 0x02,                      # Feature (Data, Variable, Absolute)
    0xC0,                            # End Collection

    # Report ID 4 - LampMultiUpdateReport
    0x85, 0x04,                      # Report ID (4)
    0x09, 0x50,                      # Usage (LampMultiUpdateReport)
    0xA1, 0x02,                      # Collection (Logical)
    0x09, 0x03,                      # Usage (LampCount)
    0x25, 0x08,                      # Logical Maximum (8)
    0x75, 0x08,                      # Report Size (8)
    0x95, 0x01,                      # Report Count (1)
    0xB1, 0x02,                      # Feature (Data, Variable, Absolute)
    0x09, 0x55,                      # Usage (LampUpdateFlags)
    0x25, 0x01,                      # Logical Maximum (1)
    0x75, 0x08,                      # Report Size (8)
    0x95, 0x01,                      # Report Count (1)
    0xB1, 0x02,                      # Feature (Data, Variable, Absolute)
    0x09, 0x21,                      # Usage (LampId)
    0x27, 0xFF, 0xFF, 0x00, 0x00,    # Logical Maximum (65535)
    0x75, 0x10,                      # Report Size (16)
    0x95, 0x08,                      # Report Count (8)
    0xB1, 0x02,                      # Feature (Data, Variable, Absolute)
    0x09, 0x51,                      # Usage (RedUpdateChannel)
    0x09, 0x52,                      # Usage (GreenUpdateChannel)
    0x09, 0x53,                      # Usage (BlueUpdateChannel)
    0x09, 0x54,                      # Usage (IntensityUpdateChannel)
    0x26, 0xFF, 0x00,                # Logical Maximum (255)
    0x75, 0x08,                      # Report Size (8)
    0x95, 0x20,                      # Report Count (32)
    0xB1, 0x02,                      # Feature (Data, Variable, Absolute)
    0xC0,                            # End Collection

    # Report ID 5 - LampRangeUpdateReport
    0x85, 0x05,                      # Report ID (5)
    0x09, 0x60,                      # Usage (LampRangeUpdateReport)
    0xA1, 0x02,                      # Collection (Logical)
    0x09, 0x55,                      # Usage (LampUpdateFlags)
    0x25, 0x01,                      # Logical Maximum (1)
    0x75, 0x08,                      # Report Size (8)
    0x95, 0x01,                      # Report Count (1)
    0xB1, 0x02,                      # Feature (Data, Variable, Absolute)
    0x09, 0x61,                      # Usage (LampIdStart)
    0x09, 0x62,                      # Usage (LampIdEnd)
    0x27, 0xFF, 0xFF, 0x00, 0x00,    # Logical Maximum (65535)
    0x75, 0x10,                      # Report Size (16)
    0x95, 0x02,                      # Report Count (2)
    0xB1, 0x02,                      # Feature (Data, Variable, Absolute)
    0x09, 0x51,                      # Usage (RedUpdateChannel)
    0x09, 0x52,                      # Usage (GreenUpdateChannel)
    0x09, 0x53,                      # Usage (BlueUpdateChannel)
    0x09, 0x54,                      # Usage (IntensityUpdateChannel)
    0x26, 0xFF, 0x00,                # Logical Maximum (255)
    0x75, 0x08,                      # Report Size (8)
    0x95, 0x04,                      # Report Count (4)
    0xB1, 0x02,                      # Feature (Data, Variable, Absolute)
    0xC0,                            # End Collection

    # Report ID 6 - LampArrayControlReport
    0x85, 0x06,                      # Report ID (6)
    0x09, 0x70,                      # Usage (LampArrayControlReport)
    0xA1, 0x02,                      # Collection (Logical)
    0x09, 0x71,                      # Usage (AutonomousMode)
    0x25, 0x01,                      # Logical Maximum (1)
    0x75, 0x08,                      # Report Size (8)
    0x95, 0x01,                      # Report Count (1)
    0xB1, 0x02,                      # Feature (Data, Variable, Absolute)
    0xC0,                            # End Collection

    0xC0                             # End Collection (Application)
))

lamparray = usb_hid.Device(
    report_descriptor=HID_LAMPARRAY_REPORT_DESCRIPTOR,
    usage_page=0x59,  # Usage Page for Lighting and Illumination
    usage=0x01,       # Usage ID for Lamp Array
    report_ids=(1, 2, 3, 4, 5, 6),  # Report IDs
    in_report_lengths=(21, 2, 39, 50, 9, 1),  # IN Report lengths
    out_report_lengths=(21, 2, 39, 50, 9, 1)  # OUT Report lengths
)

usb_hid.enable(
    (lamparray,)
)
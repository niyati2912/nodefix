KNOWLEDGE_BASE = [

    {
        "equipment": "ESP32",
        "title": "ESP32 Relay Wiring Guide",
        "content": (
            "Verify common ground between the ESP32 and relay module. "
            "Check relay VCC and GND connections. "
            "Verify that the GPIO pin defined in the software "
            "matches the physical relay input pin."
        )
    },

    {
        "equipment": "ESP32",
        "title": "ESP32 Power Troubleshooting SOP",
        "content": (
            "Verify the USB or regulated power source. "
            "Check for loose wiring. "
            "Confirm that the board powers correctly before "
            "testing peripheral devices."
        )
    },

    {
        "equipment": "Arduino",
        "title": "Arduino Digital Output Guide",
        "content": (
            "Check pin configuration and ensure the selected pin "
            "is configured as OUTPUT. Verify wiring between the "
            "Arduino and connected module."
        )
    },

    {
        "equipment": "Relay Module",
        "title": "Relay Module Troubleshooting SOP",
        "content": (
            "Verify supply voltage, common ground and signal input. "
            "Do not assume a relay is defective before checking "
            "power and control connections."
        )
    },

    {
        "equipment": "Sensor",
        "title": "Basic Sensor Troubleshooting Guide",
        "content": (
            "Check power, ground and signal connections. "
            "Verify the expected output range and confirm that "
            "the software is reading the correct sensor pin."
        )
    }

]


def search_documents(equipment: str, query: str):

    matches = []

    for document in KNOWLEDGE_BASE:

        if document["equipment"].lower() == equipment.lower():

            matches.append(document)

    return matches[:3]
# =========================================================
# NODEFIX VISION SERVICE
#
# CURRENT:
# Local demo / image acknowledgement
#
# LATER:
# Microsoft Foundry multimodal model
# =========================================================


def analyze_image(image_path, equipment):

    """
    Temporary local image analysis.

    Azure multimodal analysis will replace this function later.
    """

    if not image_path:

        return {
            "detected": False,
            "observation": (
                "No image was provided."
            ),
            "confidence": "N/A"
        }


    return {
        "detected": True,

        "observation": (
            f"Image received for {equipment}. "
            "A multimodal AI model will inspect the uploaded "
            "equipment image in the Azure-enabled version."
        ),

        "confidence": "Demo"
    }
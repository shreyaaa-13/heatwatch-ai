
def make_advisory(region, temperature_c, risk):
    """Generate an educational heat-safety advisory."""

    precautions = {
        "Low": (
            "Maintain normal hydration and keep checking local weather updates."
        ),
        "Moderate": (
            "Drink water regularly, reduce strenuous outdoor activity "
            "during the hottest hours, and check on vulnerable people."
        ),
        "High": (
            "Limit outdoor activity during peak heat, seek shade or a "
            "cool indoor space, hydrate regularly, and check on older "
            "adults and children."
        ),
        "Extreme": (
            "Avoid strenuous outdoor activity, move to a cool location, "
            "hydrate safely, and follow official local authority guidance. "
            "Seek urgent medical help for signs of heat illness."
        ),
    }

    precaution = precautions.get(
        risk,
        "Stay hydrated and follow local weather guidance."
    )

    return (
        f"{region}: the latest sample temperature is "
        f"{temperature_c:.1f} °C. "
        f"Prototype heat-risk level: {risk}. "
        f"{precaution} "
        "This is an educational advisory, not an official IMD warning."
    )

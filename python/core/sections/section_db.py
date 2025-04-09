from .section import Section
from .HEA import HEA
from .HEM import HEM
from .HEB import HEB
from .IPE import IPE


def select_section(section: str) -> Section:
    """
    Select a section from the sections database.

    Args:
        section (str): The name of the section to select.

    Returns:
        Section: The selected section.
    """

    s = next((s for s in HEA + HEM + HEB + IPE if s["profile"] == section), None)

    if not s:
        raise ValueError(f"Section {section} not found in database.")

    # Convert the section dictionary to a Section object
    return Section(**s)


# HEA100: Section = Section(
#     profile="HEA100",
#     g=None,
#     h=None,
#     b=None,
#     tw=None,
#     tf=None,
#     r=None,
#     A=None,
#     Iy=None,
#     iy=None,
#     Wely=None,
#     Wply=None,
#     Iz=None,
#     iz=None,
#     Welz=None,
#     Wplz=None,
#     J=None,
#     Cw=None,
# )


# secs = []
# for s in HEM:
#     s["Iy"] = int(s["Iy"] * 1000000)
#     s["Iz"] = int(s["Iz"] * 1000000)
#     s["J"] = int(s["J"] * 1000)
#     s["Cw"] = int(s["Cw"] * 1000000)
#     s["Wely"] = int(s["Wely"] * 1000)
#     s["Welz"] = int(s["Welz"] * 1000)
#     s["Wply"] = int(s["Wply"] * 1000)
#     s["Wplz"] = int(s["Wplz"] * 1000)
#     x = Section(**s)
#     secs.append(x)
# HEA_Sections = [Section(**s) for s in HEA]

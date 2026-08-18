"""Human-readable fault/error name catalog for Gecko spa packs.

Ported verbatim from GeckoLib.Product.Error.{ePackError, SpaPackError, eInClearError,
InClearError} in the official in.touch2 app (decompiled .NET IL, v2.11.0). geckolib
currently only surfaces raw numeric/tag fault codes from STATP/the status-array; this
layers friendly names on top. Read-only, no new protocol verbs -- pure lookup tables.

The string values are the "SpaPackStructureTag" names geckolib's existing driver/packs/*.py
files already use to address named accessors in the per-model status/config struct -- grep
a given model's pack file for one of these tags to confirm it's wired up for that hardware
generation before relying on it.
"""

from __future__ import annotations

from enum import IntEnum


class GeckoPackError(IntEnum):
    """ePackError -- spa control-board fault codes."""

    SUPPLY_ERROR = 0
    REMOTE_HEATER_COMM_ERROR = 1
    REMOTE_HEATER_INCOMPATIBLE = 2
    RELAY_STUCK = 3
    SLAVE_RELAY_STUCK = 4
    HIGH_LIMIT_ERROR = 5
    SLAVE_HIGH_LIMIT_ERROR = 6
    THERMAL_FUSE_ERROR = 7
    SLAVE_THERMAL_FUSE_ERROR = 8
    KIN_NO_FLO_ERROR = 9
    SLAVE_KIN_NO_FLO_ERROR = 10
    KIN_PUMP_OFF = 11
    SLAVE_KIN_PUMP_OFF = 12
    PROBE_ERROR_REG = 13
    PROBE_ERROR_TRIAC_PR = 14
    PROBE_ERROR_TRIAC_OH = 15
    PROBE_ERROR_KIN = 16
    SLAVE_PROBE_ERROR = 17
    AMBIANT_OVERHEAT_LEVEL_1 = 18
    AMBIANT_OVERHEAT_LEVEL_2 = 19
    SLAVE_AMBIANT_OVERHEAT_LEVEL_2 = 20
    OVERHEAT_ERROR = 21
    SLAVE_OVERHEAT_ERROR = 22
    SCAN_ERROR = 23
    FUSE_1_ERROR = 24
    FUSE_2_ERROR = 25
    FUSE_3_ERROR = 26
    NO_FLO_ERROR = 27
    SLAVE_NO_FLO_ERROR = 28
    FLOW_SWITCH_ERROR = 29
    THERMISTOR_ERROR = 30
    SLAVE_THERMISTOR_ERROR = 31
    SLAVE_MISSING_ERROR = 32
    NONE = 33


# ePackError -> friendly display name (the enum's own name, human-cased) and the
# SpaPackStructureTag string used to look this fault's live bit up in a pack config file.
PACK_ERROR_INFO: dict[GeckoPackError, tuple[str, str | None]] = {
    GeckoPackError.SUPPLY_ERROR: ("Supply Error", "SupplyErr"),
    GeckoPackError.REMOTE_HEATER_COMM_ERROR: ("Remote Heater Comm Error", "RhCommErr"),
    GeckoPackError.REMOTE_HEATER_INCOMPATIBLE: ("Remote Heater Incompatible", "rHId"),
    GeckoPackError.RELAY_STUCK: ("Relay Stuck", "RelayStuck"),
    GeckoPackError.SLAVE_RELAY_STUCK: ("Slave Relay Stuck", "SlaveRelayStuck"),
    GeckoPackError.HIGH_LIMIT_ERROR: ("High Limit Error", "RhHwHL"),
    GeckoPackError.SLAVE_HIGH_LIMIT_ERROR: ("Slave High Limit Error", "SlaveHLErr"),
    GeckoPackError.THERMAL_FUSE_ERROR: ("Thermal Fuse Error", "ThermFuseErr"),
    GeckoPackError.SLAVE_THERMAL_FUSE_ERROR: (
        "Slave Thermal Fuse Error",
        "SlaveThermFuseErr",
    ),
    GeckoPackError.KIN_NO_FLO_ERROR: ("No Flow Error (Kinetic)", "RhHrKinNoFlo"),
    GeckoPackError.SLAVE_KIN_NO_FLO_ERROR: (
        "Slave No Flow Error (Kinetic)",
        "SlaveKinNoFloErr",
    ),
    GeckoPackError.KIN_PUMP_OFF: ("Kinetic Pump Off", "KinPumpOff"),
    GeckoPackError.SLAVE_KIN_PUMP_OFF: ("Slave Kinetic Pump Off", "SlaveKinPumpOff"),
    GeckoPackError.PROBE_ERROR_REG: ("Probe Error (Regulation)", "RhRegProbeErr"),
    GeckoPackError.PROBE_ERROR_TRIAC_PR: ("Probe Error (Triac PR)", "RhHrTriacPr"),
    GeckoPackError.PROBE_ERROR_TRIAC_OH: ("Probe Error (Triac OH)", "RhHrTriacOH"),
    GeckoPackError.PROBE_ERROR_KIN: ("Probe Error (Kinetic)", "RhHrKin"),
    GeckoPackError.SLAVE_PROBE_ERROR: ("Slave Probe Error", "SlaveRegProbeErr"),
    GeckoPackError.AMBIANT_OVERHEAT_LEVEL_1: (
        "Ambient Overheat (Level 1)",
        "AmbiantOHLevel1",
    ),
    GeckoPackError.AMBIANT_OVERHEAT_LEVEL_2: (
        "Ambient Overheat (Level 2)",
        "AmbiantOHLevel2",
    ),
    GeckoPackError.SLAVE_AMBIANT_OVERHEAT_LEVEL_2: (
        "Slave Ambient Overheat (Level 2)",
        "SlaveAmbiantOHLevel2",
    ),
    GeckoPackError.OVERHEAT_ERROR: ("Overheat Error", "RegOverHeat"),
    GeckoPackError.SLAVE_OVERHEAT_ERROR: ("Slave Overheat Error", "SlaveRegOverHeat"),
    GeckoPackError.SCAN_ERROR: ("Scan Error", "ScanErr"),
    GeckoPackError.FUSE_1_ERROR: ("Fuse 1 Error", "Fuse1Err"),
    GeckoPackError.FUSE_2_ERROR: ("Fuse 2 Error", "Fuse2Err"),
    GeckoPackError.FUSE_3_ERROR: ("Fuse 3 Error", "Fuse3Err"),
    GeckoPackError.NO_FLO_ERROR: ("No Flow Error", "RhNoFloXTries"),
    GeckoPackError.SLAVE_NO_FLO_ERROR: ("Slave No Flow Error", "SlaveNoFloErr"),
    GeckoPackError.FLOW_SWITCH_ERROR: ("Flow Switch Error", "FLCErr"),
    GeckoPackError.THERMISTOR_ERROR: ("Thermistor Error", "ThermistanceErr"),
    GeckoPackError.SLAVE_THERMISTOR_ERROR: (
        "Slave Thermistor Error",
        "SlaveThermistanceErr",
    ),
    GeckoPackError.SLAVE_MISSING_ERROR: ("Slave Missing Error", "SlaveMissingErr"),
    GeckoPackError.NONE: ("No Fault", None),
}


class GeckoInClearError(IntEnum):
    """eInClearError -- InClear salt/mineral system fault codes."""

    LO_SUPPLY_ERROR = 0  # "LoSypplyError" in Gecko's own source (typo preserved upstream)
    COMPATIBILITY_ERROR = 1
    FLO_ERROR = 2
    HI_SALT_ERROR = 3
    LO_SALT_ERROR = 4
    HI_SALT_WARNING = 5
    LO_SALT_WARNING = 6
    NONE = 7


INCLEAR_ERROR_INFO: dict[GeckoInClearError, tuple[str, str | None]] = {
    GeckoInClearError.LO_SUPPLY_ERROR: ("Low Supply Error", "LoSupplyError"),
    GeckoInClearError.COMPATIBILITY_ERROR: (
        "Compatibility Error",
        "CompatibilityError",
    ),
    GeckoInClearError.FLO_ERROR: ("Flow Error", "FloError"),
    GeckoInClearError.HI_SALT_ERROR: ("High Salt Error", "HiSaltError"),
    GeckoInClearError.LO_SALT_ERROR: ("Low Salt Error", "LoSaltError"),
    GeckoInClearError.HI_SALT_WARNING: ("High Salt Warning", "HiSaltWarning"),
    GeckoInClearError.LO_SALT_WARNING: ("Low Salt Warning", "LoSaltWarning"),
    GeckoInClearError.NONE: ("No Fault", None),
}


class GeckoConnectionError(IntEnum):
    """eInTouchCommunicationError -- connection-level errors, distinct from spa hardware faults."""

    UNREACHABLE_CO = 0
    INCOMPLETE_CONNECTION = 1
    TOO_MANY_DEVICE = 2
    CONNECTION_LOST = 3


CONNECTION_ERROR_NAMES: dict[GeckoConnectionError, str] = {
    GeckoConnectionError.UNREACHABLE_CO: "Unreachable",
    GeckoConnectionError.INCOMPLETE_CONNECTION: "Incomplete Connection",
    GeckoConnectionError.TOO_MANY_DEVICE: "Too Many Devices",
    GeckoConnectionError.CONNECTION_LOST: "Connection Lost",
}


def pack_error_name(code: int) -> str:
    """Look up a friendly name for a raw ePackError code, falling back to the number."""
    try:
        return PACK_ERROR_INFO[GeckoPackError(code)][0]
    except ValueError:
        return f"Unknown Fault ({code})"


def inclear_error_name(code: int) -> str:
    """Look up a friendly name for a raw eInClearError code, falling back to the number."""
    try:
        return INCLEAR_ERROR_INFO[GeckoInClearError(code)][0]
    except ValueError:
        return f"Unknown InClear Fault ({code})"

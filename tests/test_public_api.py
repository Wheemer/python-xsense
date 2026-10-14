import importlib
from importlib import metadata

import pytest

import xsense
from xsense import AsyncXSense, Device, House, MQTTHelper, Station
from xsense.base import XSenseBase


def test_top_level_exports_async_client_and_models_only():
    assert xsense.__version__ == "0.1.0"
    assert xsense.__all__ == [
        "AsyncXSense",
        "camera_addx_serial",
    "camera_for_identifier",
    "camera_identifiers",
    "camera_matches_identifier",
    "camera_primary_identifiers",
    "cameras_share_identity",
    "Device",
        "House",
        "MQTTHelper",
        "Station",
        "__version__",
    ]
    assert AsyncXSense is xsense.AsyncXSense
    assert Device is xsense.Device
    assert House is xsense.House
    assert MQTTHelper is xsense.MQTTHelper
    assert Station is xsense.Station
    assert not hasattr(xsense, "XSense")


def test_distribution_metadata_matches_upstream_package():
    assert metadata.version("python-xsense") == xsense.__version__
    dist = metadata.metadata("python-xsense")
    assert dist["Name"] == "python-xsense"
    assert dist["Requires-Python"] == ">=3.10"
    assert dist.get_all("Provides-Extra") == ["test", "dev"]
    requirements = metadata.requires("python-xsense") or []
    assert "paho-mqtt<3,>=2.1.0" in requirements


def test_sync_client_module_was_removed():
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("xsense.xsense")


def test_cognito_login_keeps_sync_login_compatibility_alias():
    assert XSenseBase._cognito_login is XSenseBase.sync_login


def test_async_client_exposes_current_camera_api_surface():
    assert hasattr(AsyncXSense, "update_camera_sleep")
    assert hasattr(AsyncXSense, "update_camera_cooldown")
    assert hasattr(AsyncXSense, "update_camera_recording_resolution")
    assert hasattr(AsyncXSense, "update_camera_default_codec")


def test_event_parser_has_explicit_public_exports():
    event_parser = importlib.import_module("xsense.event_parser")

    assert "mqtt_reported_data" in event_parser.__all__
    assert "camera_event_records" in event_parser.__all__
    assert "apply_apk_ai_detection_aliases" in event_parser.__all__
    assert "normalize_self_test_report" in event_parser.__all__
    assert "is_presence_topic" in event_parser.__all__


def test_webrtc_signal_exports_current_relay_surface():
    webrtc_signal = importlib.import_module("xsense.webrtc_signal")

    assert hasattr(webrtc_signal, "XSenseWebRTCTicket")
    assert hasattr(webrtc_signal, "XSenseWebRTCSignalSession")
    assert hasattr(webrtc_signal, "make_sdp_offer_payload")
    assert hasattr(webrtc_signal, "make_ice_candidate_payload")
    assert hasattr(webrtc_signal, "parse_signal_message")

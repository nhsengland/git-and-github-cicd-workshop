"""Shared test infrastructure for the practice_level_gp_appointments package.

Loguru mock fixtures are provided here for tests that need to assert
on logging behaviour.
"""

import pytest


# ── Loguru mock fixtures ──────────────────────────────────────────────────────


@pytest.fixture
def mock_info(mocker):
    return mocker.patch("loguru.logger.info")


@pytest.fixture
def mock_warning(mocker):
    return mocker.patch("loguru.logger.warning")


@pytest.fixture
def mock_error(mocker):
    return mocker.patch("loguru.logger.error")


@pytest.fixture
def mock_success(mocker):
    return mocker.patch("loguru.logger.success")


@pytest.fixture
def mock_debug(mocker):
    return mocker.patch("loguru.logger.debug")


@pytest.fixture
def mock_log_levels(
    mock_info, mock_warning, mock_error, mock_success, mock_debug
):
    return {
        "info": mock_info,
        "warning": mock_warning,
        "error": mock_error,
        "success": mock_success,
        "debug": mock_debug,
    }

"""Tests for practice_level_gp_appointments.pipeline."""

import pytest

from practice_level_gp_appointments.pipeline import NHSPracticeAnalysisPipeline


@pytest.fixture
def mock_config(mocker):
    return mocker.MagicMock()


class TestNHSPracticeAnalysisPipelineRunAnalysis:
    """Tests for NHSPracticeAnalysisPipeline.run_analysis."""

    def test_returns_zero_on_successful_run(self, mock_config, mocker):
        """run_analysis() returns 0 when validate() and run() both succeed."""
        pipeline = NHSPracticeAnalysisPipeline(mock_config)
        mocker.patch.object(pipeline, "validate")
        mocker.patch.object(pipeline, "run")

        result = pipeline.run_analysis()

        assert result == 0

    def test_returns_one_when_validation_fails(self, mock_config, mocker):
        """run_analysis() returns 1 when validate() raises an exception."""
        pipeline = NHSPracticeAnalysisPipeline(mock_config)
        mocker.patch.object(
            pipeline, "validate", side_effect=ValueError("invalid config")
        )

        result = pipeline.run_analysis()

        assert result == 1

    def test_returns_one_when_pipeline_run_fails(self, mock_config, mocker):
        """run_analysis() returns 1 when run() raises an exception."""
        pipeline = NHSPracticeAnalysisPipeline(mock_config)
        mocker.patch.object(pipeline, "validate")
        mocker.patch.object(
            pipeline, "run", side_effect=RuntimeError("stage failed")
        )

        result = pipeline.run_analysis()

        assert result == 1

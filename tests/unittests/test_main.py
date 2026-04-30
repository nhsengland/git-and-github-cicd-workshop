"""Tests for practice_level_gp_appointments.__main__."""

import pytest

from practice_level_gp_appointments.__main__ import (
    main,
    practice_level_gp_appointments_main,
)


class TestPracticeLevelGpAppointmentsMain:
    """Tests for practice_level_gp_appointments_main()."""

    def test_returns_zero_on_successful_pipeline_run(self, mocker):
        """Returns 0 when config creation and pipeline execution both succeed."""
        mocker.patch(
            "practice_level_gp_appointments.__main__.NHSPracticeAnalysisConfig.create"
        )
        mock_pipeline_cls = mocker.patch(
            "practice_level_gp_appointments.__main__.NHSPracticeAnalysisPipeline"
        )
        mock_pipeline_cls.return_value.run_analysis.return_value = 0

        result = practice_level_gp_appointments_main("jul_25")

        assert result == 0

    def test_returns_one_when_zip_file_not_found(self, mocker):
        """Returns 1 when NHSPracticeAnalysisConfig.create raises FileNotFoundError."""
        mocker.patch(
            "practice_level_gp_appointments.__main__.NHSPracticeAnalysisConfig.create",
            side_effect=FileNotFoundError(
                "Zip file not found: data/compressed/bad.zip"
            ),
        )

        result = practice_level_gp_appointments_main("bad_stem")

        assert result == 1

    def test_returns_one_when_pipeline_raises_exception(self, mocker):
        """Returns 1 when the pipeline raises an unexpected exception."""
        mocker.patch(
            "practice_level_gp_appointments.__main__.NHSPracticeAnalysisConfig.create"
        )
        mock_pipeline_cls = mocker.patch(
            "practice_level_gp_appointments.__main__.NHSPracticeAnalysisPipeline"
        )
        mock_pipeline_cls.return_value.run_analysis.side_effect = RuntimeError(
            "unexpected failure"
        )

        result = practice_level_gp_appointments_main("jul_25")

        assert result == 1


class TestMain:
    """Tests for main() CLI entry point."""

    def test_uses_default_jul_25_stem_when_no_args_provided(self, mocker):
        """Calls pipeline main with 'jul_25' when --zip-file-stem is not given."""
        mocker.patch("sys.argv", ["prog"])
        mock_runner = mocker.patch(
            "practice_level_gp_appointments.__main__.practice_level_gp_appointments_main",
            return_value=0,
        )

        main()

        mock_runner.assert_called_once_with("jul_25")

    def test_passes_custom_zip_file_stem_to_pipeline_main(self, mocker):
        """Passes the --zip-file-stem argument value to practice_level_gp_appointments_main."""
        mocker.patch("sys.argv", ["prog", "--zip-file-stem", "aug_25"])
        mock_runner = mocker.patch(
            "practice_level_gp_appointments.__main__.practice_level_gp_appointments_main",
            return_value=0,
        )

        main()

        mock_runner.assert_called_once_with("aug_25")

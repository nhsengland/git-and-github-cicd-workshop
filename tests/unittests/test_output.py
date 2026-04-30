"""Tests for practice_level_gp_appointments.output."""

import pandas as pd
import pytest

from practice_level_gp_appointments.output import OutputStage


@pytest.fixture
def mock_config(mocker, tmp_path):
    config = mocker.MagicMock()
    config.processed_data_dir = tmp_path / "processed"
    config.figures_dir = tmp_path / "figures"
    config.figure_format = "png"
    config.figure_dpi = 300
    config.figure_bbox_inches = "tight"
    return config


@pytest.fixture
def sample_context(mock_config):
    """Minimal pipeline context for OutputStage: data, summaries, and no figures."""
    combined = pd.DataFrame(
        {
            "gp_code": ["A", "B"],
            "count_of_appointments": [100, 200],
            "data_month": ["may_25", "jun_25"],
        }
    )
    summaries = {
        "monthly_by_status": pd.DataFrame(
            {
                "data_month": ["may_25"],
                "appt_status": ["Attended"],
                "count": [100],
            }
        )
    }
    return {
        "combined_data": combined,
        "summary_statistics": summaries,
        "figures": {},
    }


class TestOutputStageInit:
    """Tests for OutputStage.__init__."""

    def test_stage_name(self, mock_config):
        """Stage is registered with the name 'output'."""
        stage = OutputStage(mock_config)
        assert stage.name == "output"

    def test_inputs(self, mock_config):
        """Stage reads from combined_data, summary_statistics, and figures."""
        stage = OutputStage(mock_config)
        assert stage.input_keys == (
            "combined_data",
            "summary_statistics",
            "figures",
        )

    def test_stores_config(self, mock_config):
        """Config object is accessible as stage.config."""
        stage = OutputStage(mock_config)
        assert stage.config is mock_config


class TestOutputStageRun:
    """Tests for OutputStage.run."""

    def test_creates_processed_output_directory(
        self, mock_config, sample_context
    ):
        """run() creates the processed data directory if it does not exist."""
        assert not mock_config.processed_data_dir.exists()
        OutputStage(mock_config).run(sample_context)
        assert mock_config.processed_data_dir.exists()

    def test_saves_combined_data_csv(self, mock_config, sample_context):
        """run() saves combined_data.csv in the processed directory."""
        OutputStage(mock_config).run(sample_context)
        assert (mock_config.processed_data_dir / "combined_data.csv").exists()

    def test_combined_data_csv_has_correct_row_count(
        self, mock_config, sample_context
    ):
        """Saved combined_data.csv contains every row from the input DataFrame."""
        OutputStage(mock_config).run(sample_context)
        saved = pd.read_csv(
            mock_config.processed_data_dir / "combined_data.csv"
        )
        assert len(saved) == 2

    def test_saves_summary_table_csv(self, mock_config, sample_context):
        """run() saves each summary table as a CSV named after its key."""
        OutputStage(mock_config).run(sample_context)
        assert (
            mock_config.processed_data_dir / "monthly_by_status.csv"
        ).exists()

    def test_output_files_recorded_in_context(
        self, mock_config, sample_context
    ):
        """run() stores a dict of output paths in context['output_files']."""
        OutputStage(mock_config).run(sample_context)
        assert "output_files" in sample_context
        assert "combined_data" in sample_context["output_files"]

"""Tests for practice_level_gp_appointments.data_processing."""

from pathlib import Path

import pandas as pd
import pytest

from practice_level_gp_appointments.data_processing import (
    DataExtractionStage,
    DataJoiningStage,
    DataLoadingStage,
)


@pytest.fixture
def mock_config(mocker):
    return mocker.MagicMock()


# ── DataExtractionStage ───────────────────────────────────────────────────────


class TestDataExtractionStageInit:
    """Tests for DataExtractionStage.__init__."""

    def test_stage_name(self, mock_config):
        """Stage is registered with the name 'data_extraction'."""
        stage = DataExtractionStage(mock_config)
        assert stage.name == "data_extraction"

    def test_outputs(self, mock_config):
        """Stage writes to 'extracted_files'."""
        stage = DataExtractionStage(mock_config)
        assert stage.output_keys == ("extracted_files",)

    def test_stores_config(self, mock_config):
        """Config object is accessible as stage.config."""
        stage = DataExtractionStage(mock_config)
        assert stage.config is mock_config


class TestDataExtractionStageRun:
    """Tests for DataExtractionStage.run."""

    def test_returns_context_when_zip_file_missing(self, mock_config):
        """run() stores an empty file list and returns context when zip absent."""
        mock_config.input_zip_file = Path("nonexistent.zip")
        context = {}
        result = DataExtractionStage(mock_config).run(context)
        assert result is context
        assert context["extracted_files"] == []

    def test_extracts_csv_files_from_zip(self, mock_config, tmp_path):
        """run() extracts CSV files into raw_data_dir."""
        import zipfile

        zip_path = tmp_path / "data.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("may_25.csv", "col\n1\n2")

        raw_dir = tmp_path / "raw"
        mock_config.input_zip_file = zip_path
        mock_config.raw_data_dir = raw_dir
        mock_config.lookup_data_dir = tmp_path / "lookup"

        context = {}
        DataExtractionStage(mock_config).run(context)

        assert (raw_dir / "may_25.csv").exists()

    def test_routes_mapping_csv_to_lookup_dir(self, mock_config, tmp_path):
        """run() places files with 'mapping' in the name into lookup_data_dir."""
        import zipfile

        zip_path = tmp_path / "data.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("Mapping.csv", "gp_code,icb_code\nA,ICB1")

        lookup_dir = tmp_path / "lookup"
        mock_config.input_zip_file = zip_path
        mock_config.raw_data_dir = tmp_path / "raw"
        mock_config.lookup_data_dir = lookup_dir

        context = {}
        DataExtractionStage(mock_config).run(context)

        assert (lookup_dir / "Mapping.csv").exists()


# ── DataLoadingStage ──────────────────────────────────────────────────────────


class TestDataLoadingStageInit:
    """Tests for DataLoadingStage.__init__."""

    def test_stage_name(self, mock_config):
        """Stage is registered with the name 'data_loading'."""
        stage = DataLoadingStage(mock_config)
        assert stage.name == "data_loading"

    def test_inputs(self, mock_config):
        """Stage reads from 'extracted_files'."""
        stage = DataLoadingStage(mock_config)
        assert stage.input_keys == ("extracted_files",)

    def test_outputs(self, mock_config):
        """Stage writes to 'raw_data'."""
        stage = DataLoadingStage(mock_config)
        assert stage.output_keys == ("raw_data",)


class TestDataLoadingStageDiscoverCsvFiles:
    """Tests for DataLoadingStage._discover_csv_files."""

    def test_returns_all_csv_files_in_raw_dir(self, mocker, tmp_path):
        """Discovers all CSV files matching the configured pattern."""
        raw_dir = tmp_path / "raw" / "jul_25"
        raw_dir.mkdir(parents=True)
        (raw_dir / "may_25.csv").write_text("col\n1")
        (raw_dir / "jun_25.csv").write_text("col\n2")

        config = mocker.MagicMock()
        config.raw_data_dir = raw_dir
        config.csv_file_pattern = "*.csv"

        result = DataLoadingStage(config)._discover_csv_files()

        assert set(result.keys()) == {"may_25", "jun_25"}

    def test_returns_empty_dict_when_no_csv_files_present(
        self, mocker, tmp_path
    ):
        """Returns an empty dict when the raw directory contains no CSVs."""
        raw_dir = tmp_path / "raw"
        raw_dir.mkdir()

        config = mocker.MagicMock()
        config.raw_data_dir = raw_dir
        config.csv_file_pattern = "*.csv"

        result = DataLoadingStage(config)._discover_csv_files()

        assert result == {}


# ── DataJoiningStage ──────────────────────────────────────────────────────────


class TestDataJoiningStageInit:
    """Tests for DataJoiningStage.__init__."""

    def test_stage_name(self):
        """Stage is registered with the name 'data_joining'."""
        stage = DataJoiningStage()
        assert stage.name == "data_joining"

    def test_inputs(self):
        """Stage reads from 'raw_data'."""
        stage = DataJoiningStage()
        assert stage.input_keys == ("raw_data",)

    def test_outputs(self):
        """Stage writes to 'combined_data'."""
        stage = DataJoiningStage()
        assert stage.output_keys == ("combined_data",)


class TestDataJoiningStageRun:
    """Tests for DataJoiningStage.run."""

    def test_concatenates_all_monthly_dataframes(self):
        """Rows from all non-mapping datasets are combined into one DataFrame."""
        context = {
            "raw_data": {
                "may_25": pd.DataFrame(
                    {"gp_code": ["A"], "count_of_appointments": [100]}
                ),
                "jun_25": pd.DataFrame(
                    {"gp_code": ["B"], "count_of_appointments": [200]}
                ),
            }
        }
        DataJoiningStage().run(context)
        assert len(context["combined_data"]) == 2

    def test_adds_data_month_identifier_column(self):
        """Each row has a data_month column matching its source dataset key."""
        context = {
            "raw_data": {
                "may_25": pd.DataFrame(
                    {"gp_code": ["A"], "count_of_appointments": [1]}
                ),
                "jun_25": pd.DataFrame(
                    {"gp_code": ["B"], "count_of_appointments": [2]}
                ),
            }
        }
        DataJoiningStage().run(context)
        result = context["combined_data"]
        assert set(result["data_month"]) == {"may_25", "jun_25"}

    def test_merges_mapping_data_on_gp_code(self):
        """region_name and icb columns from mapping appear in the joined output."""
        context = {
            "raw_data": {
                "may_25": pd.DataFrame(
                    {"gp_code": ["A"], "count_of_appointments": [100]}
                ),
                "mapping": pd.DataFrame(
                    {
                        "gp_code": ["A"],
                        "icb_code": ["ICB1"],
                        "icb_name": ["ICB One"],
                        "region_code": ["R1"],
                        "region_name": ["Region One"],
                    }
                ),
            }
        }
        DataJoiningStage().run(context)
        result = context["combined_data"]
        assert "region_name" in result.columns
        assert list(result["region_name"]) == ["Region One"]

    def test_raises_value_error_when_no_monthly_data(self):
        """Raises ValueError when raw_data contains only mapping (no monthly data)."""
        context = {
            "raw_data": {
                "mapping": pd.DataFrame({"gp_code": ["A"]}),
            }
        }
        with pytest.raises(ValueError, match="No monthly data found"):
            DataJoiningStage().run(context)

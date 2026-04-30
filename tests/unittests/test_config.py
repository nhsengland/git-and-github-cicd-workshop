"""Tests for practice_level_gp_appointments.config."""

from pathlib import Path

import pytest

from practice_level_gp_appointments.config import NHSPracticeAnalysisConfig


class TestNHSPracticeAnalysisConfigCreate:
    """Tests for NHSPracticeAnalysisConfig.create()."""

    def test_raises_file_not_found_when_zip_missing(self):
        """Raises FileNotFoundError when the zip file does not exist."""
        with pytest.raises(FileNotFoundError, match="Zip file not found"):
            NHSPracticeAnalysisConfig.create("nonexistent_stem")

    def test_creates_correct_raw_data_dir(self, mocker):
        """raw_data_dir is data/raw/<stem>."""
        mocker.patch("pathlib.Path.exists", return_value=True)
        config = NHSPracticeAnalysisConfig.create("jul_25")
        assert config.raw_data_dir == Path("data/raw/jul_25")

    def test_creates_correct_figures_dir(self, mocker):
        """figures_dir is figures/<stem>."""
        mocker.patch("pathlib.Path.exists", return_value=True)
        config = NHSPracticeAnalysisConfig.create("jul_25")
        assert config.figures_dir == Path("figures/jul_25")

    def test_creates_correct_output_dir(self, mocker):
        """output_dir is data/processed/<stem>."""
        mocker.patch("pathlib.Path.exists", return_value=True)
        config = NHSPracticeAnalysisConfig.create("jul_25")
        assert config.output_dir == Path("data/processed/jul_25")

    def test_creates_correct_zip_path(self, mocker):
        """input_zip_file is data/compressed/<stem>.zip."""
        mocker.patch("pathlib.Path.exists", return_value=True)
        config = NHSPracticeAnalysisConfig.create("jul_25")
        assert config.input_zip_file == Path("data/compressed/jul_25.zip")

    def test_date_id_matches_stem(self, mocker):
        """date_id is set to the zip_file_stem argument."""
        mocker.patch("pathlib.Path.exists", return_value=True)
        config = NHSPracticeAnalysisConfig.create("jul_25")
        assert config.date_id == "jul_25"

    def test_custom_stem_sets_all_paths_correctly(self, mocker):
        """All date-specific paths update when a custom stem is provided."""
        mocker.patch("pathlib.Path.exists", return_value=True)
        config = NHSPracticeAnalysisConfig.create("aug_25")
        assert config.date_id == "aug_25"
        assert config.raw_data_dir == Path("data/raw/aug_25")
        assert config.figures_dir == Path("figures/aug_25")
        assert config.input_zip_file == Path("data/compressed/aug_25.zip")


class TestNHSPracticeAnalysisConfigDefaults:
    """Tests for NHSPracticeAnalysisConfig Pydantic field default values."""

    def test_default_csv_file_pattern(self):
        """csv_file_pattern defaults to '*.csv'."""
        assert (
            NHSPracticeAnalysisConfig.model_fields["csv_file_pattern"].default
            == "*.csv"
        )

    def test_default_lookup_file(self):
        """lookup_file defaults to 'Mapping.csv'."""
        assert (
            NHSPracticeAnalysisConfig.model_fields["lookup_file"].default
            == "Mapping.csv"
        )

    def test_default_figure_format(self):
        """figure_format defaults to 'png'."""
        assert (
            NHSPracticeAnalysisConfig.model_fields["figure_format"].default
            == "png"
        )

    def test_default_figure_dpi(self):
        """figure_dpi defaults to 300."""
        assert (
            NHSPracticeAnalysisConfig.model_fields["figure_dpi"].default == 300
        )

    def test_default_sample_size_is_none(self):
        """sample_size defaults to None (no sampling)."""
        assert (
            NHSPracticeAnalysisConfig.model_fields["sample_size"].default
            is None
        )

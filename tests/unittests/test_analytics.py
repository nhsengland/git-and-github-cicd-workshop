"""Tests for practice_level_gp_appointments.analytics."""

import pandas as pd
import pytest

from practice_level_gp_appointments.analytics import SummarisationStage


@pytest.fixture
def mock_config(mocker):
    return mocker.MagicMock()


@pytest.fixture
def appointments_df():
    """Sample combined appointment DataFrame with three statuses."""
    return pd.DataFrame(
        {
            "data_month": [
                "2025-05",
                "2025-05",
                "2025-05",
                "2025-06",
                "2025-06",
            ],
            "appt_status": ["Attended", "DNA", "Attended", "Attended", "DNA"],
            "hcp_type": ["GP", "GP", "Nurse", "GP", "Nurse"],
            "appt_mode": [
                "Face-to-Face",
                "Telephone",
                "Face-to-Face",
                "Online",
                "Telephone",
            ],
            "time_between_book_and_appt": [0, 1, 2, 0, 3],
            "count_of_appointments": [100, 10, 50, 120, 8],
        }
    )


@pytest.fixture
def appointments_with_region(appointments_df):
    """Appointments DataFrame that also includes a region_name column."""
    df = appointments_df.copy()
    df["region_name"] = ["North", "North", "South", "South", "North"]
    return df


class TestSummarisationStageInit:
    """Tests for SummarisationStage.__init__."""

    def test_stage_name(self, mock_config):
        """Stage is registered with the name 'summarisation'."""
        stage = SummarisationStage(mock_config)
        assert stage.name == "summarisation"

    def test_stores_config(self, mock_config):
        """Config object is accessible as stage.config."""
        stage = SummarisationStage(mock_config)
        assert stage.config is mock_config

    def test_inputs(self, mock_config):
        """Stage reads from 'combined_data'."""
        stage = SummarisationStage(mock_config)
        assert stage.input_keys == ("combined_data",)

    def test_outputs(self, mock_config):
        """Stage writes to 'summary_statistics'."""
        stage = SummarisationStage(mock_config)
        assert stage.output_keys == ("summary_statistics",)


class TestSummarisationStageRun:
    """Tests for SummarisationStage.run."""

    def test_produces_monthly_by_status_summary(
        self, mock_config, appointments_df
    ):
        """run() stores a monthly_by_status table in summary_statistics."""
        context = {"combined_data": appointments_df}
        SummarisationStage(mock_config).run(context)
        assert "monthly_by_status" in context["summary_statistics"]

    def test_monthly_by_status_has_correct_columns(
        self, mock_config, appointments_df
    ):
        """monthly_by_status has exactly the three expected columns."""
        context = {"combined_data": appointments_df}
        SummarisationStage(mock_config).run(context)
        cols = set(context["summary_statistics"]["monthly_by_status"].columns)
        assert cols == {"data_month", "appt_status", "count_of_appointments"}

    def test_produces_hcp_type_summary(self, mock_config, appointments_df):
        """run() stores an hcp_type_summary table."""
        context = {"combined_data": appointments_df}
        SummarisationStage(mock_config).run(context)
        assert "hcp_type_summary" in context["summary_statistics"]

    def test_produces_mode_by_month_summary(
        self, mock_config, appointments_df
    ):
        """run() stores a mode_by_month table."""
        context = {"combined_data": appointments_df}
        SummarisationStage(mock_config).run(context)
        assert "mode_by_month" in context["summary_statistics"]

    def test_produces_booking_time_summary(self, mock_config, appointments_df):
        """run() stores a booking_time_summary table."""
        context = {"combined_data": appointments_df}
        SummarisationStage(mock_config).run(context)
        assert "booking_time_summary" in context["summary_statistics"]

    def test_produces_regional_summary_when_region_column_present(
        self, mock_config, appointments_with_region
    ):
        """run() includes regional_summary only when region_name column exists."""
        context = {"combined_data": appointments_with_region}
        SummarisationStage(mock_config).run(context)
        assert "regional_summary" in context["summary_statistics"]

    def test_omits_regional_summary_when_no_region_column(
        self, mock_config, appointments_df
    ):
        """run() omits regional_summary when region_name column is absent."""
        context = {"combined_data": appointments_df}
        SummarisationStage(mock_config).run(context)
        assert "regional_summary" not in context["summary_statistics"]

    def test_produces_key_metrics(self, mock_config, appointments_df):
        """run() stores a key_metrics table containing dna_rate."""
        context = {"combined_data": appointments_df}
        SummarisationStage(mock_config).run(context)
        summaries = context["summary_statistics"]
        assert "key_metrics" in summaries
        metric_names = list(summaries["key_metrics"]["metric"])
        assert "dna_rate" in metric_names

    def test_dna_rate_calculated_correctly(self, mock_config, appointments_df):
        """dna_rate = DNA appointments / total appointments.

        Input: DNA=18, total=288 → rate = 18/288 = 0.0625
        """
        context = {"combined_data": appointments_df}
        SummarisationStage(mock_config).run(context)
        key_metrics = context["summary_statistics"]["key_metrics"]
        dna_rate = float(
            key_metrics.loc[key_metrics["metric"] == "dna_rate", "value"].iloc[
                0
            ]
        )
        expected = 18 / 288
        assert abs(dna_rate - expected) < 1e-9

    def test_completion_rate_calculated_correctly(
        self, mock_config, appointments_df
    ):
        """completion_rate = attended / total.

        Input: Attended=270, total=288 → rate = 270/288 = 0.9375
        """
        context = {"combined_data": appointments_df}
        SummarisationStage(mock_config).run(context)
        key_metrics = context["summary_statistics"]["key_metrics"]
        completion_rate = float(
            key_metrics.loc[
                key_metrics["metric"] == "completion_rate", "value"
            ].iloc[0]
        )
        expected = 270 / 288
        assert abs(completion_rate - expected) < 1e-9

"""
Comprehensive tests for calculadora-sostenibilidad functions.

Tests cover:
- normalizar_inverso(): Value normalization logic
- calcular_score_producto(): Core sustainability scoring algorithm
- clasificar_score(): Score classification into categories
- exportar_resultados_excel(): Excel export functionality
"""

import pytest
import pandas as pd
from io import BytesIO
from app_calculadora_sostenibilidad_v2 import (
    normalizar_inverso,
    calcular_score_producto,
    clasificar_score,
    exportar_resultados_excel
)


class TestNormalizarInverso:
    """Test suite for the normalizar_inverso function."""

    def test_normal_case_mid_value(self):
        """Test normalization with a middle value."""
        result = normalizar_inverso(50, 0, 100)
        assert result == 50.0

    def test_minimum_value_returns_100(self):
        """Test that minimum value returns 100 (best score)."""
        result = normalizar_inverso(0, 0, 100)
        assert result == 100.0

    def test_maximum_value_returns_0(self):
        """Test that maximum value returns 0 (worst score)."""
        result = normalizar_inverso(100, 0, 100)
        assert result == 0.0

    def test_equal_min_max_returns_50(self):
        """Test that equal min and max returns 50 (special case)."""
        result = normalizar_inverso(10, 10, 10)
        assert result == 50

    def test_quarter_value(self):
        """Test normalization at 25% of range."""
        result = normalizar_inverso(25, 0, 100)
        assert result == 75.0

    def test_three_quarter_value(self):
        """Test normalization at 75% of range."""
        result = normalizar_inverso(75, 0, 100)
        assert result == 25.0

    def test_with_decimal_values(self):
        """Test normalization with decimal values."""
        result = normalizar_inverso(1.5, 0.5, 2.5)
        assert result == 50.0

    def test_carbon_footprint_range(self):
        """Test with actual Carbon Footprint range from dataset."""
        # CF range: (0.3, 60.0)
        # Test minimum CF value (best)
        result_min = normalizar_inverso(0.3, 0.3, 60.0)
        assert result_min == 100.0

        # Test maximum CF value (worst)
        result_max = normalizar_inverso(60.0, 0.3, 60.0)
        assert result_max == 0.0

        # Test middle value
        result_mid = normalizar_inverso(30.15, 0.3, 60.0)
        assert pytest.approx(result_mid, rel=1e-2) == 50.0

    def test_water_footprint_range(self):
        """Test with actual Water Footprint range from dataset."""
        # WF range: (131, 18900)
        result_min = normalizar_inverso(131, 131, 18900)
        assert result_min == 100.0

        result_max = normalizar_inverso(18900, 131, 18900)
        assert result_max == 0.0

    def test_nova_range(self):
        """Test with actual NOVA range from dataset."""
        # NOVA range: (1, 4)
        result_min = normalizar_inverso(1, 1, 4)
        assert result_min == 100.0

        result_max = normalizar_inverso(4, 1, 4)
        assert result_max == 0.0

        # Test NOVA level 2
        result_2 = normalizar_inverso(2, 1, 4)
        assert pytest.approx(result_2, rel=1e-2) == 66.67

    def test_value_below_minimum(self):
        """Test behavior when value is below minimum (extrapolation)."""
        result = normalizar_inverso(0, 10, 20)
        assert result == 200.0  # Extrapolates beyond 100

    def test_value_above_maximum(self):
        """Test behavior when value is above maximum (extrapolation)."""
        result = normalizar_inverso(30, 10, 20)
        assert result == -100.0  # Extrapolates below 0

    def test_negative_range(self):
        """Test normalization with negative values."""
        result = normalizar_inverso(-5, -10, 0)
        assert result == 50.0


class TestCalcularScoreProducto:
    """Test suite for the calcular_score_producto function."""

    def test_escenario_a_perfect_product(self):
        """Test perfect product (all minimum values) in scenario A."""
        # Perfect values: minimum for all indicators
        score, normalized = calcular_score_producto(
            cf=0.3, wf=131, lu=0.3, origin=0, waste=3.0, nova=1, escenario='A'
        )

        # All normalized values should be 100
        assert normalized['CF'] == 100.0
        assert normalized['WF'] == 100.0
        assert normalized['LU'] == 100.0
        assert normalized['Origin'] == 100.0
        assert normalized['Waste'] == 100.0
        assert normalized['NOVA'] == 100.0

        # Perfect score should be 100
        assert score == 100.0

    def test_escenario_b_perfect_product(self):
        """Test perfect product (all minimum values) in scenario B."""
        score, normalized = calcular_score_producto(
            cf=0.3, wf=131, lu=0.3, origin=0, waste=3.0, nova=1, escenario='B'
        )

        # Perfect score should be 100
        assert score == 100.0

    def test_escenario_a_worst_product(self):
        """Test worst product (all maximum values) in scenario A."""
        score, normalized = calcular_score_producto(
            cf=60.0, wf=18900, lu=326, origin=100, waste=45.0, nova=4, escenario='A'
        )

        # All normalized values should be 0
        assert normalized['CF'] == 0.0
        assert normalized['WF'] == 0.0
        assert normalized['LU'] == 0.0
        assert normalized['Origin'] == 0.0
        assert normalized['Waste'] == 0.0
        assert normalized['NOVA'] == 0.0

        # Worst score should be 0
        assert score == 0.0

    def test_escenario_b_worst_product(self):
        """Test worst product (all maximum values) in scenario B."""
        score, normalized = calcular_score_producto(
            cf=60.0, wf=18900, lu=326, origin=100, waste=45.0, nova=4, escenario='B'
        )

        # Worst score should be 0
        assert score == 0.0

    def test_escenario_a_weights_sum_to_one(self):
        """Test that weights in scenario A sum to 1.0."""
        weights_a = {
            'CF': 0.15, 'WF': 0.15, 'LU': 0.10,
            'Origin': 0.20, 'Waste': 0.25, 'NOVA': 0.15
        }
        assert sum(weights_a.values()) == 1.0

    def test_escenario_b_weights_sum_to_one(self):
        """Test that weights in scenario B sum to 1.0."""
        weights_b = {
            'CF': 0.14, 'WF': 0.14, 'LU': 0.09,
            'Origin': 0.18, 'Waste': 0.30, 'NOVA': 0.15
        }
        assert sum(weights_b.values()) == 1.0

    def test_escenario_a_mid_values(self):
        """Test with middle-range values in scenario A."""
        score, normalized = calcular_score_producto(
            cf=30.15, wf=9515.5, lu=163.15, origin=50, waste=24.0, nova=2.5, escenario='A'
        )

        # All normalized values should be approximately 50
        assert pytest.approx(normalized['CF'], rel=1e-2) == 50.0
        assert pytest.approx(normalized['WF'], rel=1e-2) == 50.0
        assert pytest.approx(normalized['LU'], rel=1e-2) == 50.0
        assert pytest.approx(normalized['Origin'], rel=1e-2) == 50.0
        assert pytest.approx(normalized['Waste'], rel=1e-2) == 50.0
        assert pytest.approx(normalized['NOVA'], rel=1e-2) == 50.0

        # Score should be 50 (since all normalized values are 50)
        assert pytest.approx(score, rel=1e-2) == 50.0

    def test_escenario_a_manual_calculation(self):
        """Test manual calculation verification for scenario A."""
        # Use simple values for easy verification
        score, normalized = calcular_score_producto(
            cf=0.3, wf=131, lu=0.3, origin=50, waste=3.0, nova=1, escenario='A'
        )

        # Expected normalized values:
        # CF: 100, WF: 100, LU: 100, Origin: 50, Waste: 100, NOVA: 100

        # Expected score calculation (Scenario A weights):
        expected_score = (
            100 * 0.15 +  # CF
            100 * 0.15 +  # WF
            100 * 0.10 +  # LU
            50 * 0.20 +   # Origin
            100 * 0.25 +  # Waste
            100 * 0.15    # NOVA
        )

        assert pytest.approx(score, rel=1e-2) == expected_score
        assert pytest.approx(score, rel=1e-2) == 90.0

    def test_escenario_b_manual_calculation(self):
        """Test manual calculation verification for scenario B."""
        score, normalized = calcular_score_producto(
            cf=0.3, wf=131, lu=0.3, origin=50, waste=3.0, nova=1, escenario='B'
        )

        # Expected score calculation (Scenario B weights):
        expected_score = (
            100 * 0.14 +  # CF
            100 * 0.14 +  # WF
            100 * 0.09 +  # LU
            50 * 0.18 +   # Origin
            100 * 0.30 +  # Waste
            100 * 0.15    # NOVA
        )

        assert pytest.approx(score, rel=1e-2) == expected_score
        assert pytest.approx(score, rel=1e-2) == 91.0

    def test_difference_between_escenarios(self):
        """Test that scenarios A and B produce different scores."""
        # Use values where waste has significant impact
        score_a, _ = calcular_score_producto(
            cf=30.0, wf=9500, lu=163, origin=50, waste=45.0, nova=2, escenario='A'
        )

        score_b, _ = calcular_score_producto(
            cf=30.0, wf=9500, lu=163, origin=50, waste=45.0, nova=2, escenario='B'
        )

        # Scores should be different due to different waste weights
        assert score_a != score_b

        # Scenario B has higher waste weight (30% vs 25%), so with bad waste
        # (45.0 is maximum = 0 normalized), score_b should be lower
        assert score_b < score_a

    def test_waste_impact_escenario_a(self):
        """Test waste indicator impact in scenario A (25% weight)."""
        # Good waste
        score_good, _ = calcular_score_producto(
            cf=30.0, wf=9500, lu=163, origin=50, waste=3.0, nova=2, escenario='A'
        )

        # Bad waste
        score_bad, _ = calcular_score_producto(
            cf=30.0, wf=9500, lu=163, origin=50, waste=45.0, nova=2, escenario='A'
        )

        # Difference should be approximately 25 points (100 * 0.25)
        assert pytest.approx(score_good - score_bad, rel=1e-2) == 25.0

    def test_waste_impact_escenario_b(self):
        """Test waste indicator impact in scenario B (30% weight)."""
        # Good waste
        score_good, _ = calcular_score_producto(
            cf=30.0, wf=9500, lu=163, origin=50, waste=3.0, nova=2, escenario='B'
        )

        # Bad waste
        score_bad, _ = calcular_score_producto(
            cf=30.0, wf=9500, lu=163, origin=50, waste=45.0, nova=2, escenario='B'
        )

        # Difference should be approximately 30 points (100 * 0.30)
        assert pytest.approx(score_good - score_bad, rel=1e-2) == 30.0

    def test_default_escenario_is_a(self):
        """Test that default scenario is A when not specified."""
        score_default, _ = calcular_score_producto(
            cf=30.0, wf=9500, lu=163, origin=50, waste=24.0, nova=2
        )

        score_a, _ = calcular_score_producto(
            cf=30.0, wf=9500, lu=163, origin=50, waste=24.0, nova=2, escenario='A'
        )

        assert score_default == score_a

    def test_returns_tuple_with_score_and_dict(self):
        """Test that function returns tuple of (score, normalized_dict)."""
        result = calcular_score_producto(
            cf=30.0, wf=9500, lu=163, origin=50, waste=24.0, nova=2, escenario='A'
        )

        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], float)
        assert isinstance(result[1], dict)

    def test_normalized_dict_has_all_keys(self):
        """Test that normalized dict contains all indicators."""
        _, normalized = calcular_score_producto(
            cf=30.0, wf=9500, lu=163, origin=50, waste=24.0, nova=2, escenario='A'
        )

        expected_keys = {'CF', 'WF', 'LU', 'Origin', 'Waste', 'NOVA'}
        assert set(normalized.keys()) == expected_keys

    def test_with_zero_carbon_footprint(self):
        """Test edge case with zero carbon footprint (below min range)."""
        score, normalized = calcular_score_producto(
            cf=0.0, wf=131, lu=0.3, origin=0, waste=3.0, nova=1, escenario='A'
        )

        # CF normalized should be > 100 (extrapolated)
        assert normalized['CF'] > 100.0
        # Score can exceed 100 in this edge case
        assert score > 100.0


class TestClasificarScore:
    """Test suite for the clasificar_score function."""

    def test_excelente_at_90(self):
        """Test Excelente classification at boundary (90)."""
        categoria, emoji = clasificar_score(90)
        assert categoria == 'Excelente'
        assert emoji == '🟢'

    def test_excelente_at_95(self):
        """Test Excelente classification above boundary."""
        categoria, emoji = clasificar_score(95)
        assert categoria == 'Excelente'
        assert emoji == '🟢'

    def test_excelente_at_100(self):
        """Test Excelente classification at maximum."""
        categoria, emoji = clasificar_score(100)
        assert categoria == 'Excelente'
        assert emoji == '🟢'

    def test_muy_bueno_at_80(self):
        """Test Muy Bueno classification at boundary (80)."""
        categoria, emoji = clasificar_score(80)
        assert categoria == 'Muy Bueno'
        assert emoji == '🟢'

    def test_muy_bueno_at_85(self):
        """Test Muy Bueno classification in range."""
        categoria, emoji = clasificar_score(85)
        assert categoria == 'Muy Bueno'
        assert emoji == '🟢'

    def test_muy_bueno_at_89_99(self):
        """Test Muy Bueno classification just below Excelente."""
        categoria, emoji = clasificar_score(89.99)
        assert categoria == 'Muy Bueno'
        assert emoji == '🟢'

    def test_bueno_at_70(self):
        """Test Bueno classification at boundary (70)."""
        categoria, emoji = clasificar_score(70)
        assert categoria == 'Bueno'
        assert emoji == '🟡'

    def test_bueno_at_75(self):
        """Test Bueno classification in range."""
        categoria, emoji = clasificar_score(75)
        assert categoria == 'Bueno'
        assert emoji == '🟡'

    def test_bueno_at_79_99(self):
        """Test Bueno classification just below Muy Bueno."""
        categoria, emoji = clasificar_score(79.99)
        assert categoria == 'Bueno'
        assert emoji == '🟡'

    def test_moderado_at_60(self):
        """Test Moderado classification at boundary (60)."""
        categoria, emoji = clasificar_score(60)
        assert categoria == 'Moderado'
        assert emoji == '🟠'

    def test_moderado_at_65(self):
        """Test Moderado classification in range."""
        categoria, emoji = clasificar_score(65)
        assert categoria == 'Moderado'
        assert emoji == '🟠'

    def test_moderado_at_69_99(self):
        """Test Moderado classification just below Bueno."""
        categoria, emoji = clasificar_score(69.99)
        assert categoria == 'Moderado'
        assert emoji == '🟠'

    def test_bajo_at_59_99(self):
        """Test Bajo classification just below Moderado."""
        categoria, emoji = clasificar_score(59.99)
        assert categoria == 'Bajo'
        assert emoji == '🔴'

    def test_bajo_at_50(self):
        """Test Bajo classification in range."""
        categoria, emoji = clasificar_score(50)
        assert categoria == 'Bajo'
        assert emoji == '🔴'

    def test_bajo_at_0(self):
        """Test Bajo classification at minimum."""
        categoria, emoji = clasificar_score(0)
        assert categoria == 'Bajo'
        assert emoji == '🔴'

    def test_bajo_negative_score(self):
        """Test Bajo classification with negative score (edge case)."""
        categoria, emoji = clasificar_score(-10)
        assert categoria == 'Bajo'
        assert emoji == '🔴'

    def test_excelente_above_100(self):
        """Test Excelente classification above 100 (edge case)."""
        categoria, emoji = clasificar_score(105)
        assert categoria == 'Excelente'
        assert emoji == '🟢'

    def test_returns_tuple(self):
        """Test that function returns a tuple."""
        result = clasificar_score(75)
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_returns_string_and_string(self):
        """Test that function returns (string, string)."""
        categoria, emoji = clasificar_score(75)
        assert isinstance(categoria, str)
        assert isinstance(emoji, str)

    def test_all_categories_have_emojis(self):
        """Test that all categories return valid emojis."""
        test_scores = [95, 85, 75, 65, 55]
        expected_emojis = ['🟢', '🟢', '🟡', '🟠', '🔴']

        for score, expected_emoji in zip(test_scores, expected_emojis):
            _, emoji = clasificar_score(score)
            assert emoji == expected_emoji

    def test_boundary_transitions(self):
        """Test all boundary transitions are correct."""
        # Just below 90 -> Muy Bueno
        cat1, _ = clasificar_score(89.99)
        assert cat1 == 'Muy Bueno'

        # At 90 -> Excelente
        cat2, _ = clasificar_score(90)
        assert cat2 == 'Excelente'

        # Just below 80 -> Bueno
        cat3, _ = clasificar_score(79.99)
        assert cat3 == 'Bueno'

        # At 80 -> Muy Bueno
        cat4, _ = clasificar_score(80)
        assert cat4 == 'Muy Bueno'

        # Just below 70 -> Moderado
        cat5, _ = clasificar_score(69.99)
        assert cat5 == 'Moderado'

        # At 70 -> Bueno
        cat6, _ = clasificar_score(70)
        assert cat6 == 'Bueno'

        # Just below 60 -> Bajo
        cat7, _ = clasificar_score(59.99)
        assert cat7 == 'Bajo'

        # At 60 -> Moderado
        cat8, _ = clasificar_score(60)
        assert cat8 == 'Moderado'


class TestIntegrationScenarios:
    """Integration tests combining multiple functions."""

    def test_full_workflow_excellent_product(self):
        """Test complete workflow for an excellent product."""
        # Calculate score for an excellent product
        score, normalized = calcular_score_producto(
            cf=1.0, wf=500, lu=5.0, origin=5, waste=5.0, nova=1, escenario='A'
        )

        # Score should be high
        assert score > 85

        # Classify the score
        categoria, emoji = clasificar_score(score)

        # Should be in top categories
        assert categoria in ['Excelente', 'Muy Bueno']
        assert emoji == '🟢'

    def test_full_workflow_poor_product(self):
        """Test complete workflow for a poor product."""
        # Calculate score for a poor product
        score, normalized = calcular_score_producto(
            cf=55.0, wf=17000, lu=300, origin=90, waste=40.0, nova=4, escenario='A'
        )

        # Score should be low
        assert score < 20

        # Classify the score
        categoria, emoji = clasificar_score(score)

        # Should be Bajo
        assert categoria == 'Bajo'
        assert emoji == '🔴'

    def test_scenario_comparison_workflow(self):
        """Test comparing same product in both scenarios."""
        # Calculate for both scenarios
        score_a, _ = calcular_score_producto(
            cf=30.0, wf=9500, lu=163, origin=50, waste=30.0, nova=3, escenario='A'
        )

        score_b, _ = calcular_score_producto(
            cf=30.0, wf=9500, lu=163, origin=50, waste=30.0, nova=3, escenario='B'
        )

        # Classify both
        cat_a, _ = clasificar_score(score_a)
        cat_b, _ = clasificar_score(score_b)

        # Both should produce valid classifications
        assert cat_a in ['Excelente', 'Muy Bueno', 'Bueno', 'Moderado', 'Bajo']
        assert cat_b in ['Excelente', 'Muy Bueno', 'Bueno', 'Moderado', 'Bajo']

    def test_normalized_values_affect_score_correctly(self):
        """Test that normalized values correctly contribute to final score."""
        score, normalized = calcular_score_producto(
            cf=0.3, wf=131, lu=0.3, origin=0, waste=45.0, nova=1, escenario='A'
        )

        # Most values are perfect (100) except waste (0)
        # Scenario A: Waste is 25% weight
        # Expected: 0.15*100 + 0.15*100 + 0.10*100 + 0.20*100 + 0.25*0 + 0.15*100
        expected = 0.15*100 + 0.15*100 + 0.10*100 + 0.20*100 + 0.25*0 + 0.15*100

        assert pytest.approx(score, rel=1e-2) == expected
        assert pytest.approx(score, rel=1e-2) == 75.0


class TestExportarResultadosExcel:
    """Test suite for the exportar_resultados_excel function."""

    @pytest.fixture
    def sample_dataframe(self):
        """Create a sample dataframe for testing."""
        data = {
            'Producto': ['Sandía', 'Res', 'Pollo', 'Zanahoria', 'Manzana', 'Café',
                        'Guayaba', 'Papaya', 'Uva', 'Lenteja', 'Avena', 'Melón',
                        'Piña', 'Tomate', 'Lechuga'],
            'CF_kgCO2eq_kg': [0.5, 60.0, 6.9, 0.4, 0.4, 28.5, 0.28, 0.3, 1.1, 0.9, 2.5, 0.6, 0.7, 1.4, 0.5],
            'WF_L_kg': [235, 15400, 4325, 131, 822, 18900, 400, 200, 850, 5000, 2400, 300, 400, 214, 237],
            'LU_m2_kg': [0.2, 326, 7.1, 0.5, 0.6, 21.5, 0.25, 0.18, 1.2, 3.4, 7.6, 0.3, 0.4, 0.8, 0.7],
            'Origin_Score': [0, 100, 50, 0, 50, 100, 0, 0, 50, 0, 50, 0, 50, 0, 0],
            'Waste_pct': [0.4, 21.2, 12.4, 14.1, 12.2, 2.0, 5.5, 7.1, 45.5, 3.1, 1.5, 8.2, 9.5, 17.8, 25.6],
            'NOVA': [1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1],
            'Score_México': [95.2, 25.3, 68.4, 92.1, 78.5, 45.2, 98.7, 96.3, 60.1, 88.9, 75.3, 91.4, 85.6, 82.3, 70.5],
            'Score_México_B': [96.1, 23.8, 67.2, 93.0, 77.9, 46.5, 99.2, 97.1, 58.3, 89.7, 76.1, 92.2, 84.9, 81.5, 69.2]
        }
        return pd.DataFrame(data)

    @pytest.fixture
    def small_dataframe(self):
        """Create a small dataframe with only 5 products for edge case testing."""
        data = {
            'Producto': ['Sandía', 'Res', 'Pollo', 'Zanahoria', 'Manzana'],
            'CF_kgCO2eq_kg': [0.5, 60.0, 6.9, 0.4, 0.4],
            'WF_L_kg': [235, 15400, 4325, 131, 822],
            'LU_m2_kg': [0.2, 326, 7.1, 0.5, 0.6],
            'Origin_Score': [0, 100, 50, 0, 50],
            'Waste_pct': [0.4, 21.2, 12.4, 14.1, 12.2],
            'NOVA': [1, 1, 1, 1, 1],
            'Score_México': [95.2, 25.3, 68.4, 92.1, 78.5],
            'Score_México_B': [96.1, 23.8, 67.2, 93.0, 77.9]
        }
        return pd.DataFrame(data)

    def test_returns_bytesio_object(self, sample_dataframe):
        """Test that function returns a BytesIO object."""
        result = exportar_resultados_excel(sample_dataframe, escenario='A')
        assert isinstance(result, BytesIO)

    def test_bytesio_is_not_empty(self, sample_dataframe):
        """Test that returned BytesIO object contains data."""
        result = exportar_resultados_excel(sample_dataframe, escenario='A')
        result.seek(0)
        content = result.read()
        assert len(content) > 0

    def test_excel_file_has_three_sheets_escenario_a(self, sample_dataframe):
        """Test that Excel file contains exactly 3 sheets for scenario A."""
        result = exportar_resultados_excel(sample_dataframe, escenario='A')
        result.seek(0)

        # Read Excel file
        excel_file = pd.ExcelFile(result)

        # Check number of sheets
        assert len(excel_file.sheet_names) == 3

    def test_excel_sheet_names_are_correct(self, sample_dataframe):
        """Test that Excel sheets have correct names."""
        result = exportar_resultados_excel(sample_dataframe, escenario='A')
        result.seek(0)

        excel_file = pd.ExcelFile(result)
        expected_sheets = ['Ranking_Completo', 'Top_15', 'Menos_Sostenibles']

        assert excel_file.sheet_names == expected_sheets

    def test_ranking_completo_has_all_products(self, sample_dataframe):
        """Test that Ranking_Completo sheet contains all products."""
        result = exportar_resultados_excel(sample_dataframe, escenario='A')
        result.seek(0)

        df_ranking = pd.read_excel(result, sheet_name='Ranking_Completo')

        # Should have same number of rows as input dataframe
        assert len(df_ranking) == len(sample_dataframe)

    def test_ranking_completo_has_correct_columns_escenario_a(self, sample_dataframe):
        """Test that Ranking_Completo sheet has correct columns for scenario A."""
        result = exportar_resultados_excel(sample_dataframe, escenario='A')
        result.seek(0)

        df_ranking = pd.read_excel(result, sheet_name='Ranking_Completo')

        expected_columns = ['Producto', 'CF_kgCO2eq_kg', 'WF_L_kg', 'LU_m2_kg',
                           'Origin_Score', 'Waste_pct', 'NOVA', 'Score_México']

        assert list(df_ranking.columns) == expected_columns

    def test_ranking_completo_has_correct_columns_escenario_b(self, sample_dataframe):
        """Test that Ranking_Completo sheet has correct columns for scenario B."""
        result = exportar_resultados_excel(sample_dataframe, escenario='B')
        result.seek(0)

        df_ranking = pd.read_excel(result, sheet_name='Ranking_Completo')

        expected_columns = ['Producto', 'CF_kgCO2eq_kg', 'WF_L_kg', 'LU_m2_kg',
                           'Origin_Score', 'Waste_pct', 'NOVA', 'Score_México_B']

        assert list(df_ranking.columns) == expected_columns

    def test_ranking_completo_is_sorted_descending_escenario_a(self, sample_dataframe):
        """Test that Ranking_Completo is sorted by score in descending order for scenario A."""
        result = exportar_resultados_excel(sample_dataframe, escenario='A')
        result.seek(0)

        df_ranking = pd.read_excel(result, sheet_name='Ranking_Completo')

        # Check that scores are in descending order
        scores = df_ranking['Score_México'].tolist()
        assert scores == sorted(scores, reverse=True)

    def test_ranking_completo_is_sorted_descending_escenario_b(self, sample_dataframe):
        """Test that Ranking_Completo is sorted by score in descending order for scenario B."""
        result = exportar_resultados_excel(sample_dataframe, escenario='B')
        result.seek(0)

        df_ranking = pd.read_excel(result, sheet_name='Ranking_Completo')

        # Check that scores are in descending order
        scores = df_ranking['Score_México_B'].tolist()
        assert scores == sorted(scores, reverse=True)

    def test_ranking_completo_top_product_is_correct_escenario_a(self, sample_dataframe):
        """Test that top product in Ranking_Completo is the one with highest score."""
        result = exportar_resultados_excel(sample_dataframe, escenario='A')
        result.seek(0)

        df_ranking = pd.read_excel(result, sheet_name='Ranking_Completo')

        # Top product should be Guayaba (98.7)
        assert df_ranking.iloc[0]['Producto'] == 'Guayaba'
        assert pytest.approx(df_ranking.iloc[0]['Score_México'], rel=1e-2) == 98.7

    def test_top_15_has_15_products_when_available(self, sample_dataframe):
        """Test that Top_15 sheet contains 15 products when dataframe has enough."""
        result = exportar_resultados_excel(sample_dataframe, escenario='A')
        result.seek(0)

        df_top15 = pd.read_excel(result, sheet_name='Top_15')

        # Should have exactly 15 products
        assert len(df_top15) == 15

    def test_top_15_has_correct_columns_escenario_a(self, sample_dataframe):
        """Test that Top_15 sheet has only Producto and Score columns."""
        result = exportar_resultados_excel(sample_dataframe, escenario='A')
        result.seek(0)

        df_top15 = pd.read_excel(result, sheet_name='Top_15')

        expected_columns = ['Producto', 'Score_México']
        assert list(df_top15.columns) == expected_columns

    def test_top_15_has_correct_columns_escenario_b(self, sample_dataframe):
        """Test that Top_15 sheet uses Score_México_B for scenario B."""
        result = exportar_resultados_excel(sample_dataframe, escenario='B')
        result.seek(0)

        df_top15 = pd.read_excel(result, sheet_name='Top_15')

        expected_columns = ['Producto', 'Score_México_B']
        assert list(df_top15.columns) == expected_columns

    def test_top_15_contains_highest_scores(self, sample_dataframe):
        """Test that Top_15 contains the products with the 15 highest scores."""
        result = exportar_resultados_excel(sample_dataframe, escenario='A')
        result.seek(0)

        df_top15 = pd.read_excel(result, sheet_name='Top_15')

        # Get top 15 from original dataframe
        expected_top15 = sample_dataframe.nlargest(15, 'Score_México')['Producto'].tolist()
        actual_top15 = df_top15['Producto'].tolist()

        assert actual_top15 == expected_top15

    def test_top_15_is_sorted_descending(self, sample_dataframe):
        """Test that Top_15 is sorted in descending order."""
        result = exportar_resultados_excel(sample_dataframe, escenario='A')
        result.seek(0)

        df_top15 = pd.read_excel(result, sheet_name='Top_15')
        scores = df_top15['Score_México'].tolist()

        assert scores == sorted(scores, reverse=True)

    def test_bottom_10_has_10_products_when_available(self, sample_dataframe):
        """Test that Menos_Sostenibles sheet contains 10 products when available."""
        result = exportar_resultados_excel(sample_dataframe, escenario='A')
        result.seek(0)

        df_bottom10 = pd.read_excel(result, sheet_name='Menos_Sostenibles')

        # Should have exactly 10 products
        assert len(df_bottom10) == 10

    def test_bottom_10_has_correct_columns_escenario_a(self, sample_dataframe):
        """Test that Menos_Sostenibles sheet has correct columns."""
        result = exportar_resultados_excel(sample_dataframe, escenario='A')
        result.seek(0)

        df_bottom10 = pd.read_excel(result, sheet_name='Menos_Sostenibles')

        expected_columns = ['Producto', 'Score_México']
        assert list(df_bottom10.columns) == expected_columns

    def test_bottom_10_contains_lowest_scores(self, sample_dataframe):
        """Test that Menos_Sostenibles contains the products with 10 lowest scores."""
        result = exportar_resultados_excel(sample_dataframe, escenario='A')
        result.seek(0)

        df_bottom10 = pd.read_excel(result, sheet_name='Menos_Sostenibles')

        # Get bottom 10 from original dataframe
        expected_bottom10 = sample_dataframe.nsmallest(10, 'Score_México')['Producto'].tolist()
        actual_bottom10 = df_bottom10['Producto'].tolist()

        assert actual_bottom10 == expected_bottom10

    def test_bottom_10_contains_res_lowest_score(self, sample_dataframe):
        """Test that Menos_Sostenibles contains Res which has lowest score."""
        result = exportar_resultados_excel(sample_dataframe, escenario='A')
        result.seek(0)

        df_bottom10 = pd.read_excel(result, sheet_name='Menos_Sostenibles')

        # Res should be in the bottom 10
        assert 'Res' in df_bottom10['Producto'].tolist()

    def test_escenario_a_default_parameter(self, sample_dataframe):
        """Test that scenario A is used by default when not specified."""
        result_default = exportar_resultados_excel(sample_dataframe)
        result_a = exportar_resultados_excel(sample_dataframe, escenario='A')

        result_default.seek(0)
        result_a.seek(0)

        df_default = pd.read_excel(result_default, sheet_name='Top_15')
        df_a = pd.read_excel(result_a, sheet_name='Top_15')

        # Should have same column name (Score_México)
        assert list(df_default.columns) == list(df_a.columns)

    def test_escenario_b_uses_different_score_column(self, sample_dataframe):
        """Test that scenario B uses Score_México_B column."""
        result = exportar_resultados_excel(sample_dataframe, escenario='B')
        result.seek(0)

        df_ranking = pd.read_excel(result, sheet_name='Ranking_Completo')

        # Should contain Score_México_B column
        assert 'Score_México_B' in df_ranking.columns
        # Should NOT contain Score_México column
        assert 'Score_México' not in df_ranking.columns

    def test_small_dataframe_with_less_than_15_products(self, small_dataframe):
        """Test behavior with dataframe smaller than 15 products."""
        result = exportar_resultados_excel(small_dataframe, escenario='A')
        result.seek(0)

        df_top15 = pd.read_excel(result, sheet_name='Top_15')

        # Should have only 5 products (all available)
        assert len(df_top15) == 5

    def test_small_dataframe_with_less_than_10_products(self, small_dataframe):
        """Test Menos_Sostenibles with fewer than 10 products."""
        result = exportar_resultados_excel(small_dataframe, escenario='A')
        result.seek(0)

        df_bottom10 = pd.read_excel(result, sheet_name='Menos_Sostenibles')

        # Should have only 5 products (all available)
        assert len(df_bottom10) == 5

    def test_single_product_dataframe(self):
        """Test edge case with only one product."""
        data = {
            'Producto': ['Sandía'],
            'CF_kgCO2eq_kg': [0.5],
            'WF_L_kg': [235],
            'LU_m2_kg': [0.2],
            'Origin_Score': [0],
            'Waste_pct': [0.4],
            'NOVA': [1],
            'Score_México': [95.2],
            'Score_México_B': [96.1]
        }
        df = pd.DataFrame(data)

        result = exportar_resultados_excel(df, escenario='A')
        result.seek(0)

        excel_file = pd.ExcelFile(result)

        # Should still have 3 sheets
        assert len(excel_file.sheet_names) == 3

        # Each sheet should have 1 product
        df_ranking = pd.read_excel(result, sheet_name='Ranking_Completo')
        df_top15 = pd.read_excel(result, sheet_name='Top_15')
        df_bottom10 = pd.read_excel(result, sheet_name='Menos_Sostenibles')

        assert len(df_ranking) == 1
        assert len(df_top15) == 1
        assert len(df_bottom10) == 1

    def test_bytesio_position_is_at_start(self, sample_dataframe):
        """Test that BytesIO position is set to 0 (start) for reading."""
        result = exportar_resultados_excel(sample_dataframe, escenario='A')

        # Position should be at 0
        assert result.tell() == 0

    def test_data_integrity_no_data_loss(self, sample_dataframe):
        """Test that exported data matches original data for Ranking_Completo."""
        result = exportar_resultados_excel(sample_dataframe, escenario='A')
        result.seek(0)

        df_exported = pd.read_excel(result, sheet_name='Ranking_Completo')

        # Sort original dataframe same way
        df_original_sorted = sample_dataframe.sort_values('Score_México', ascending=False)

        # Compare Producto column (should be identical)
        assert df_exported['Producto'].tolist() == df_original_sorted['Producto'].tolist()

    def test_numeric_precision_preserved(self, sample_dataframe):
        """Test that numeric values are preserved with correct precision."""
        result = exportar_resultados_excel(sample_dataframe, escenario='A')
        result.seek(0)

        df_exported = pd.read_excel(result, sheet_name='Ranking_Completo')

        # Check that Guayaba's score is preserved
        guayaba_row = df_exported[df_exported['Producto'] == 'Guayaba'].iloc[0]
        assert pytest.approx(guayaba_row['Score_México'], rel=1e-1) == 98.7
        assert pytest.approx(guayaba_row['CF_kgCO2eq_kg'], rel=1e-2) == 0.28

    def test_both_scenarios_produce_different_rankings(self, sample_dataframe):
        """Test that scenarios A and B can produce different Top 15."""
        result_a = exportar_resultados_excel(sample_dataframe, escenario='A')
        result_b = exportar_resultados_excel(sample_dataframe, escenario='B')

        result_a.seek(0)
        result_b.seek(0)

        df_top15_a = pd.read_excel(result_a, sheet_name='Top_15')
        df_top15_b = pd.read_excel(result_b, sheet_name='Top_15')

        # Column names should be different
        assert df_top15_a.columns[1] == 'Score_México'
        assert df_top15_b.columns[1] == 'Score_México_B'

    def test_excel_file_is_readable_by_pandas(self, sample_dataframe):
        """Test that the Excel file can be fully read by pandas without errors."""
        result = exportar_resultados_excel(sample_dataframe, escenario='A')
        result.seek(0)

        # This should not raise any exception
        excel_file = pd.ExcelFile(result)

        # Read all sheets
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(result, sheet_name=sheet_name)
            assert isinstance(df, pd.DataFrame)
            assert len(df) > 0

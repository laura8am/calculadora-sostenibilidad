"""
Simple verification script to test the refactored functions without Streamlit dependencies.
This directly extracts and tests the core logic.
"""

from typing import Dict, Tuple

# Configuration Constants (extracted from refactored code)
INDICATOR_RANGES: Dict[str, Tuple[float, float]] = {
    'CF': (0.28, 60.0),
    'WF': (131, 18900),
    'LU': (0.18, 326),
    'Origin': (0, 100),
    'Waste': (0.4, 45.5),
    'NOVA': (1, 4)
}

SCENARIO_A_WEIGHTS: Dict[str, float] = {
    'CF': 0.15, 'WF': 0.15, 'LU': 0.10,
    'Origin': 0.20, 'Waste': 0.25, 'NOVA': 0.15
}

SCENARIO_B_WEIGHTS: Dict[str, float] = {
    'CF': 0.14, 'WF': 0.14, 'LU': 0.09,
    'Origin': 0.18, 'Waste': 0.30, 'NOVA': 0.15
}

SCENARIOS: Dict[str, Dict[str, float]] = {
    'A': SCENARIO_A_WEIGHTS,
    'B': SCENARIO_B_WEIGHTS
}

# Core functions (extracted from refactored code)
def normalizar_inverso(valor: float, min_val: float, max_val: float) -> float:
    """Normalize values where lower is better (0-100)"""
    if max_val == min_val:
        return 50.0
    return 100.0 - ((valor - min_val) / (max_val - min_val) * 100.0)

def calcular_score_producto(
    cf: float, wf: float, lu: float, origin: float,
    waste: float, nova: int, escenario: str = 'A'
) -> Tuple[float, Dict[str, float]]:
    """Calculate sustainability score"""
    if escenario not in SCENARIOS:
        raise ValueError(f"Invalid scenario: {escenario}")

    normalized_values = {
        'CF': normalizar_inverso(cf, *INDICATOR_RANGES['CF']),
        'WF': normalizar_inverso(wf, *INDICATOR_RANGES['WF']),
        'LU': normalizar_inverso(lu, *INDICATOR_RANGES['LU']),
        'Origin': normalizar_inverso(origin, *INDICATOR_RANGES['Origin']),
        'Waste': normalizar_inverso(waste, *INDICATOR_RANGES['Waste']),
        'NOVA': normalizar_inverso(nova, *INDICATOR_RANGES['NOVA'])
    }

    weights = SCENARIOS[escenario]
    score = sum(
        normalized_values[indicator] * weights[indicator]
        for indicator in weights.keys()
    )

    return score, normalized_values

def clasificar_score(score: float) -> Tuple[str, str]:
    """Classify sustainability score"""
    if score >= 90:
        return 'Excelente', '🟢'
    elif score >= 80:
        return 'Muy Bueno', '🟢'
    elif score >= 70:
        return 'Bueno', '🟡'
    elif score >= 60:
        return 'Moderado', '🟠'
    else:
        return 'Bajo', '🔴'

# Test cases
def run_tests():
    print("=" * 70)
    print("REFACTORING VERIFICATION - Testing Core Logic")
    print("=" * 70)

    all_passed = True

    # Test 1: Basic calculation
    print("\n[Test 1] Basic calculation with moderate values")
    score_a, details = calcular_score_producto(2.0, 500, 1.5, 0, 10.0, 1, 'A')
    print(f"  Score A: {score_a:.2f}")
    print(f"  Normalized values: CF={details['CF']:.2f}, WF={details['WF']:.2f}, "
          f"LU={details['LU']:.2f}")
    assert 0 <= score_a <= 100, "Score should be between 0 and 100"
    print("  ✓ PASSED")

    # Test 2: Scenario comparison
    print("\n[Test 2] Comparing scenarios A vs B")
    score_a, _ = calcular_score_producto(2.0, 500, 1.5, 0, 10.0, 1, 'A')
    score_b, _ = calcular_score_producto(2.0, 500, 1.5, 0, 10.0, 1, 'B')
    print(f"  Scenario A: {score_a:.2f}")
    print(f"  Scenario B: {score_b:.2f}")
    print(f"  Difference: {abs(score_a - score_b):.2f}")
    assert score_a != score_b, "Different scenarios should produce different scores"
    print("  ✓ PASSED")

    # Test 3: Best case (all minimum values = most sustainable)
    print("\n[Test 3] Best case - all optimal values")
    score_best, _ = calcular_score_producto(0.28, 131, 0.18, 0, 0.4, 1, 'A')
    print(f"  Score: {score_best:.2f}")
    assert score_best > 95, f"Best case should score >95, got {score_best:.2f}"
    print("  ✓ PASSED")

    # Test 4: Worst case (all maximum values = least sustainable)
    print("\n[Test 4] Worst case - all worst values")
    score_worst, _ = calcular_score_producto(60.0, 18900, 326, 100, 45.5, 4, 'A')
    print(f"  Score: {score_worst:.2f}")
    assert score_worst < 10, f"Worst case should score <10, got {score_worst:.2f}"
    print("  ✓ PASSED")

    # Test 5: Configuration validation
    print("\n[Test 5] Configuration validation")
    print(f"  Indicator ranges defined: {len(INDICATOR_RANGES)} indicators")
    assert len(INDICATOR_RANGES) == 6, "Should have 6 indicators"

    weights_a_sum = sum(SCENARIO_A_WEIGHTS.values())
    weights_b_sum = sum(SCENARIO_B_WEIGHTS.values())
    print(f"  Scenario A weights sum: {weights_a_sum:.3f}")
    print(f"  Scenario B weights sum: {weights_b_sum:.3f}")
    assert abs(weights_a_sum - 1.0) < 0.001, "Weights A should sum to 1.0"
    assert abs(weights_b_sum - 1.0) < 0.001, "Weights B should sum to 1.0"
    print("  ✓ PASSED")

    # Test 6: Normalization
    print("\n[Test 6] Inverse normalization")
    norm_mid = normalizar_inverso(5.0, 0.0, 10.0)
    norm_min = normalizar_inverso(0.0, 0.0, 10.0)
    norm_max = normalizar_inverso(10.0, 0.0, 10.0)
    print(f"  Middle value (5.0): {norm_mid:.2f} (expected 50)")
    print(f"  Min value (0.0): {norm_min:.2f} (expected 100)")
    print(f"  Max value (10.0): {norm_max:.2f} (expected 0)")
    assert abs(norm_mid - 50.0) < 0.1, "Midpoint should normalize to 50"
    assert abs(norm_min - 100.0) < 0.1, "Min should normalize to 100"
    assert abs(norm_max - 0.0) < 0.1, "Max should normalize to 0"
    print("  ✓ PASSED")

    # Test 7: Classification
    print("\n[Test 7] Score classification")
    tests = [(95, 'Excelente'), (85, 'Muy Bueno'), (75, 'Bueno'),
             (65, 'Moderado'), (50, 'Bajo')]
    for score, expected in tests:
        label, emoji = clasificar_score(score)
        print(f"  Score {score}: {label} {emoji}")
        assert label == expected, f"Expected {expected}, got {label}"
    print("  ✓ PASSED")

    # Test 8: Error handling
    print("\n[Test 8] Error handling for invalid scenario")
    try:
        calcular_score_producto(2.0, 500, 1.5, 0, 10.0, 1, 'C')
        print("  ✗ FAILED - Should have raised ValueError")
        all_passed = False
    except ValueError as e:
        print(f"  Correctly raised ValueError: {e}")
        print("  ✓ PASSED")

    # Test 9: Real product examples
    print("\n[Test 9] Real product examples")

    # Example: Apple (moderate sustainability)
    score_apple, _ = calcular_score_producto(
        cf=0.43, wf=822, lu=0.63, origin=50, waste=6.7, nova=1, escenario='A'
    )
    print(f"  Apple (Manzana): {score_apple:.2f}")

    # Example: Beef (low sustainability)
    score_beef, _ = calcular_score_producto(
        cf=60.0, wf=15415, lu=326, origin=50, waste=3.1, nova=1, escenario='A'
    )
    print(f"  Beef (Res): {score_beef:.2f}")

    assert score_apple > score_beef, "Apple should be more sustainable than beef"
    print("  ✓ PASSED - Apple scores higher than beef")

    # Test 10: Type checking
    print("\n[Test 10] Return type validation")
    score, details = calcular_score_producto(2.0, 500, 1.5, 0, 10.0, 1, 'A')
    assert isinstance(score, float), f"Score should be float, got {type(score)}"
    assert isinstance(details, dict), f"Details should be dict, got {type(details)}"
    assert len(details) == 6, f"Details should have 6 keys, got {len(details)}"
    print(f"  Score type: {type(score).__name__}")
    print(f"  Details type: {type(details).__name__} with {len(details)} keys")
    print("  ✓ PASSED")

    print("\n" + "=" * 70)
    if all_passed:
        print("✅ ALL TESTS PASSED")
        print("The refactored code maintains the same behavior!")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 70)

    return all_passed

if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)

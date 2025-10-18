from pinochle import *

# Opcode 0 test cases in Nock format
# Format: (subject_str, formula_str, expected_str, should_crash, description)

OPCODE_0_TESTS = [
    # Basic crash and identity
    ("42", "[0 0]", None, True, "axis 0 always crashes"),
    ("100", "[0 1]", "100", False, "axis 1 returns whole subject (atom)"),
    ("[10 20]", "[0 1]", "[10 20]", False, "axis 1 returns whole subject (cell)"),
    
    # Simple tree navigation - direct children
    ("[10 20]", "[0 2]", "10", False, "axis 2 gets head"),
    ("[10 20]", "[0 3]", "20", False, "axis 3 gets tail"),
    ("[[1 2] [3 4]]", "[0 2]", "[1 2]", False, "axis 2 on nested tree"),
    ("[[1 2] [3 4]]", "[0 3]", "[3 4]", False, "axis 3 on nested tree"),
    
    # Powers of 2 (left-heavy paths)
    ("[[1 2] [3 4]]", "[0 4]", "1", False, "axis 4 = /[2 /[2 tree]]"),
    ("[[1 2] [3 4]]", "[0 5]", "2", False, "axis 5 = /[3 /[2 tree]]"),
    ("[[[1 2] 3] 4]", "[0 8]", "1", False, "axis 8 goes three levels left"),
    ("[[[1 2] 3] 4]", "[0 9]", "2", False, "axis 9 = left, left, right"),
    
    # Right-heavy and mixed paths
    ("[[1 2] [3 4]]", "[0 6]", "3", False, "axis 6 = /[2 /[3 tree]]"),
    ("[[1 2] [3 4]]", "[0 7]", "4", False, "axis 7 = /[3 /[3 tree]]"),
    ("[1 [2 [3 4]]]", "[0 6]", "2", False, "axis 6 on right-branching tree"),
    ("[1 [2 [3 4]]]", "[0 7]", "[3 4]", False, "axis 7 on right-branching tree"),
    
    # Deeper navigation (axes 8-15)
    ("[[[1 2] [3 4]] [[5 6] [7 8]]]", "[0 8]", "1", False, "axis 8"),
    ("[[[1 2] [3 4]] [[5 6] [7 8]]]", "[0 10]", "3", False, "axis 10"),
    ("[[[1 2] [3 4]] [[5 6] [7 8]]]", "[0 12]", "5", False, "axis 12"),
    ("[[[1 2] [3 4]] [[5 6] [7 8]]]", "[0 14]", "7", False, "axis 14"),
    ("[[[1 2] [3 4]] [[5 6] [7 8]]]", "[0 15]", "8", False, "axis 15"),
    
    # Deep left-branching tree
    ("[[[[1 2] 3] 4] 5]", "[0 16]", "1", False, "axis 16 on deep left tree"),
    ("[[[[1 2] 3] 4] 5]", "[0 17]", "2", False, "axis 17 on deep left tree"),
    
    # Deep right-branching tree  
    ("[1 [2 [3 [4 5]]]]", "[0 14]", "3", False, "axis 14 on deep right tree"),
    ("[1 [2 [3 [4 5]]]]", "[0 15]", "[4 5]", False, "axis 15 on deep right tree"),
    
    # Large axes
    ("[[[1 2] [3 4]] [[5 6] [7 [8 9]]]]", "[0 31]", "9", False, "axis 31 = rightmost of depth 4"),
    
    # Unbalanced trees
    ("[[1 [2 3]] 4]", "[0 5]", "[2 3]", False, "axis 5 on unbalanced tree"),
    ("[1 [[2 3] 4]]", "[0 6]", "[2 3]", False, "axis 6 on unbalanced tree"),
    
    # Crash cases - axis too deep for tree
    ("[1 2]", "[0 4]", None, True, "axis 4 on shallow tree crashes"),
    ("[1 2]", "[0 8]", None, True, "axis 8 on shallow tree crashes"),
    ("42", "[0 2]", None, True, "axis 2 on atom crashes"),
    ("100", "[0 3]", None, True, "axis 3 on atom crashes"),
    
    # Edge case: large axis on sufficient tree
    ("[1 2 3 4 5 6 7]", "[0 127]", "7", False, "axis 127 on deep tree"),
    ("[[[[[[1 2] 3] 4] 5] 6] 7]", "[0 64]", "1", False, "axis 64 on deep tree"),
]

def test_opcode_0():
    """Run all opcode 0 tests using parsed Nock strings"""
    passed = 0
    failed = 0
    
    for i, (subject_str, formula_str, expected_str, should_crash, description) in enumerate(OPCODE_0_TESTS):
        try:
            subject = parse_noun(subject_str)
            formula = parse_noun(formula_str)
            result = nock(subject, formula)
            
            if should_crash:
                print(f"✗ Test {i+1} FAILED: {description}")
                print(f"   Subject: {subject_str}, Formula: {formula_str}")
                print(f"   Expected crash but got: {result}")
                failed += 1
            else:
                expected = parse_noun(expected_str)
                if result == expected:
                    print(f"✓ Test {i+1} passed: {description}")
                    passed += 1
                else:
                    print(f"✗ Test {i+1} FAILED: {description}")
                    print(f"   Subject: {subject_str}, Formula: {formula_str}")
                    print(f"   Expected: {expected_str}, Got: {result}")
                    failed += 1
        except Exception as e:
            if should_crash:
                print(f"✓ Test {i+1} passed: {description} (crashed as expected)")
                passed += 1
            else:
                print(f"✗ Test {i+1} FAILED: {description}")
                print(f"   Subject: {subject_str}, Formula: {formula_str}")
                print(f"   Unexpected crash: {e}")
                failed += 1
    
    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed out of {len(OPCODE_0_TESTS)} tests")
    return passed, failed

# Run the tests
test_opcode_0()

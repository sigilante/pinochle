from pinochle import *

# Opcode 1 test cases in Nock format
# *[a 1 b] = b (always returns the constant b, regardless of subject a)
# Format: (subject_str, formula_str, expected_str, should_crash, description)

OPCODE_1_TESTS = [
    # Small atoms
    ("42", "[1 0]", "0", False, "opcode 1 returns 0"),
    ("100", "[1 1]", "1", False, "opcode 1 returns 1"),
    ("0", "[1 2]", "2", False, "opcode 1 returns 2"),
    ("999", "[1 42]", "42", False, "opcode 1 returns 42"),
    ("1", "[1 255]", "255", False, "opcode 1 returns 255 (2^8-1)"),
    ("2", "[1 256]", "256", False, "opcode 1 returns 256 (2^8)"),
    
    # 16-bit boundaries
    ("3", "[1 65535]", "65535", False, "opcode 1 returns 2^16-1"),
    ("4", "[1 65536]", "65536", False, "opcode 1 returns 2^16"),
    
    # 31-bit boundaries (common for signed 32-bit ints)
    ("5", "[1 2147483647]", "2147483647", False, "opcode 1 returns 2^31-1"),
    ("6", "[1 2147483648]", "2147483648", False, "opcode 1 returns 2^31"),
    
    # 32-bit boundaries
    ("7", "[1 4294967295]", "4294967295", False, "opcode 1 returns 2^32-1"),
    ("8", "[1 4294967296]", "4294967296", False, "opcode 1 returns 2^32"),
    
    # 62-bit boundaries
    ("9", "[1 4611686018427387903]", "4611686018427387903", False, "opcode 1 returns 2^62-1"),
    ("10", "[1 4611686018427387904]", "4611686018427387904", False, "opcode 1 returns 2^62"),
    
    # 63-bit boundaries (common for signed 64-bit ints)
    ("11", "[1 9223372036854775807]", "9223372036854775807", False, "opcode 1 returns 2^63-1"),
    ("12", "[1 9223372036854775808]", "9223372036854775808", False, "opcode 1 returns 2^63"),
    
    # 64-bit boundaries
    ("13", "[1 18446744073709551615]", "18446744073709551615", False, "opcode 1 returns 2^64-1"),
    ("14", "[1 18446744073709551616]", "18446744073709551616", False, "opcode 1 returns 2^64"),
    
    # 128-bit atom
    ("15", "[1 340282366920938463463374607431768211455]", "340282366920938463463374607431768211455", False, "opcode 1 returns 2^128-1"),
    
    # Simple cells
    ("[1 2]", "[1 [3 4]]", "[3 4]", False, "opcode 1 returns cell [3 4]"),
    ("[5 6]", "[1 [0 0]]", "[0 0]", False, "opcode 1 returns cell [0 0]"),
    ("[[7 8] 9]", "[1 [1 1]]", "[1 1]", False, "opcode 1 returns cell [1 1]"),
    
    # Nested cells
    ("0", "[1 [[1 2] [3 4]]]", "[[1 2] [3 4]]", False, "opcode 1 returns nested cell"),
    ("100", "[1 [[[1 2] 3] 4]]", "[[[1 2] 3] 4]", False, "opcode 1 returns left-deep cell"),
    ("200", "[1 [1 [2 [3 4]]]]", "[1 [2 [3 4]]]", False, "opcode 1 returns right-deep cell"),
    
    # Complex cells with mixed structure
    ("42", "[1 [[0 1] [2 [3 [4 5]]]]]", "[[0 1] [2 [3 [4 5]]]]", False, "opcode 1 returns complex nested cell"),
    ("[100 200]", "[1 [[[1 2] [3 4]] [[5 6] [7 8]]]]", "[[[1 2] [3 4]] [[5 6] [7 8]]]", False, "opcode 1 returns balanced tree"),
    
    # Verify subject independence - same formula, different subjects
    ("0", "[1 999]", "999", False, "subject 0, constant 999"),
    ("1", "[1 999]", "999", False, "subject 1, constant 999"),
    ("123456", "[1 999]", "999", False, "subject 123456, constant 999"),
    ("[10 20]", "[1 999]", "999", False, "subject [10 20], constant 999"),
    ("[[1 2] [3 4]]", "[1 999]", "999", False, "subject nested cell, constant 999"),
    
    # Large constant with various subjects
    ("0", "[1 [1000 2000 3000]]", "[1000 [2000 3000]]", False, "multi-element cell constant"),
]

def test_opcode_1():
    """Run all opcode 1 tests"""
    passed = 0
    failed = 0
    
    for i, (subject_str, formula_str, expected_str, should_crash, description) in enumerate(OPCODE_1_TESTS):
        try:
            subject = parse(subject_str)
            formula = parse(formula_str)
            result = nock(subject, formula)
            
            if should_crash:
                print(f"✗ Test {i+1} FAILED: {description}")
                print(f"   Subject: {subject_str}, Formula: {formula_str}")
                print(f"   Expected crash but got: {result}")
                failed += 1
            else:
                expected = parse(expected_str)
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
    print(f"Results: {passed} passed, {failed} failed out of {len(OPCODE_1_TESTS)} tests")
    return passed, failed

def export_opcode_1_tests_to_hoon():
    """Export opcode 1 tests to Hoon format"""
    lines = []
    for subject_str, formula_str, expected_str, should_crash, description in OPCODE_1_TESTS:
        lines.append(f".*({subject_str} {formula_str})")
    return "\n".join(lines)

def export_opcode_1_tests_with_comments():
    """Export opcode 1 tests to Hoon format with comments"""
    lines = []
    for i, (subject_str, formula_str, expected_str, should_crash, description) in enumerate(OPCODE_1_TESTS):
        if should_crash:
            comment = f"::  Test {i+1}: {description} (should crash)"
        else:
            comment = f"::  Test {i+1}: {description} => {expected_str}"
        lines.append(comment)
        lines.append(f".*({subject_str} {formula_str})")
        lines.append("")
    return "\n".join(lines)

# Run the tests
test_opcode_1()

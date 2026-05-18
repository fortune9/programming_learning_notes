"""
Z-Algorithm Implementation
Python 3.8+ compatible

This module provides three implementations of the Z-algorithm:
1. Educational version with extensive comments
2. Clean production version
3. Pattern matching application
"""


def z_algorithm_educational(s: str) -> list:
    """
    Compute Z-array for string s using Z-algorithm.
    Educational version with extensive comments.

    Z[i] = length of longest substring starting at i that matches prefix

    Args:
        s: Input string
    Returns:
        List of integers representing Z-array
    """
    n = len(s)
    if n == 0:
        return []

    # Initialize Z-array with zeros
    z = [0] * n

    # Z[0] is undefined (we use 0 by convention)
    # Some implementations set it to n
    z[0] = 0

    # L and R define the rightmost Z-box [L, R]
    # Initially, no Z-box has been found
    left = 0
    right = 0

    # Compute Z[i] for each position from 1 to n-1
    for i in range(1, n):

        # Case 1: i is outside the current Z-box
        # We have no information to reuse, so compute naively
        if i > right:
            # Start a new Z-box at position i
            left = i
            right = i

            # Expand the Z-box as far as possible
            # Compare s[right] with s[right - left] (position in prefix)
            while right < n and s[right] == s[right - left]:
                right += 1

            # Z[i] is the length we matched
            z[i] = right - left

            # Adjust right to point to last matching character
            right -= 1

        # Case 2: i is inside the current Z-box [left, right]
        else:
            # Find mirror position k in the prefix
            k = i - left

            # How many characters remain in the current Z-box from position i?
            remaining = right - i + 1

            # Subcase 2a: Z[k] fits entirely within the remaining box
            if z[k] < remaining:
                # Safe to copy the mirror value
                z[i] = z[k]
                # No need to update L or R

            # Subcase 2b: Z[k] reaches or exceeds the box boundary
            else:
                # Copy what we know, then try to extend beyond R
                left = i

                # Continue comparing from R+1 onwards
                while right < n and s[right] == s[right - left]:
                    right += 1

                z[i] = right - left
                right -= 1

    return z


def z_algorithm(s: str) -> list:
    """
    Compute Z-array using Z-algorithm in O(n) time.

    Args:
        s: Input string
    Returns:
        Z-array where Z[i] = length of longest prefix match at position i
    """
    n = len(s)
    if n == 0:
        return []

    z = [0] * n
    left, right = 0, 0

    for i in range(1, n):
        if i > right:
            left = right = i
            while right < n and s[right] == s[right - left]:
                right += 1
            z[i] = right - left
            right -= 1
        else:
            k = i - left
            if z[k] < right - i + 1:
                z[i] = z[k]
            else:
                left = i
                while right < n and s[right] == s[right - left]:
                    right += 1
                z[i] = right - left
                right -= 1

    return z


def z_algorithm_search(text: str, pattern: str) -> list:
    """
    Find all occurrences of pattern in text using Z-algorithm.

    Args:
        text: The text to search in
        pattern: The pattern to search for
    Returns:
        List of starting indices where pattern occurs in text
    """
    if not pattern or not text:
        return []

    # Concatenate pattern and text with separator
    # Separator ensures no spurious matches across boundary
    combined = pattern + "$" + text
    z = z_algorithm(combined)

    # Find all positions where Z[i] equals pattern length
    pattern_len = len(pattern)
    matches = []

    # Start checking after pattern and separator
    for i in range(pattern_len + 1, len(combined)):
        if z[i] == pattern_len:
            # Convert to index in original text
            text_index = i - pattern_len - 1
            matches.append(text_index)

    return matches


def print_z_array(s: str, z: list) -> None:
    """Print string and Z-array aligned for easy viewing"""
    print("Position:", " ".join(f"{i:2}" for i in range(len(s))))
    print("String:  ", " ".join(f" {c}" for c in s))
    print("Z-array: ", " ".join(f"{('-' if i == 0 else str(z[i])):2}" for i in range(len(z))))


if __name__ == "__main__":
    print("=" * 60)
    print("Z-Algorithm Examples")
    print("=" * 60)

    # Example 1: Compute Z-array
    print("\n--- Example 1: Computing Z-array ---")
    s = "aabcaabxaaz"
    z = z_algorithm(s)
    print_z_array(s, z)

    # Example 2: Pattern matching
    print("\n--- Example 2: Pattern Matching ---")
    text = "ababcababcabab"
    pattern = "abab"
    matches = z_algorithm_search(text, pattern)
    print(f"Text: {text}")
    print(f"Pattern: {pattern}")
    print(f"Pattern found at positions: {matches}")

    # Verify
    for pos in matches:
        print(f"  Position {pos}: '{text[pos:pos+len(pattern)]}'")

    print("\n" + "=" * 60)

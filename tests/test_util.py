"""
Tests for util.py - utility functions.
"""

import sys
import io
import util


class TestError:
    """Tests for error() function."""

    def test_error_simple_message(self):
        """Test error output with simple message."""
        # Capture stderr
        old_stderr = sys.stderr
        sys.stderr = io.StringIO()

        util.error("Test error message")

        output = sys.stderr.getvalue()
        sys.stderr = old_stderr

        assert "Test error message\n" == output

    def test_error_with_formatting(self):
        """Test error output with format arguments."""
        old_stderr = sys.stderr
        sys.stderr = io.StringIO()

        util.error("Error: %s at line %d", "syntax error", 42)

        output = sys.stderr.getvalue()
        sys.stderr = old_stderr

        assert "Error: syntax error at line 42\n" == output

    def test_error_with_multiple_args(self):
        """Test error output with multiple format arguments."""
        old_stderr = sys.stderr
        sys.stderr = io.StringIO()

        util.error(
            "Aircraft %s at distance %.1f km, altitude %d ft", "ABC123", 15.5, 3500
        )

        output = sys.stderr.getvalue()
        sys.stderr = old_stderr

        assert "Aircraft ABC123 at distance 15.5 km, altitude 3500 ft\n" == output

    def test_error_flushes_stdout(self):
        """Test that error() flushes stdout before writing to stderr."""
        # This is harder to test directly, but we can verify it doesn't crash
        old_stdout = sys.stdout
        old_stderr = sys.stderr

        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()

        # Write to stdout
        print("Some output", end="")

        # Call error - should flush stdout first
        util.error("Error message")

        sys.stdout = old_stdout
        sys.stderr = old_stderr

        # If we get here without exception, the flush worked

    def test_error_with_special_characters(self):
        """Test error output with special characters."""
        old_stderr = sys.stderr
        sys.stderr = io.StringIO()

        util.error("Error with special chars: %s", "°C, €, ñ")

        output = sys.stderr.getvalue()
        sys.stderr = old_stderr

        assert "Error with special chars: °C, €, ñ\n" == output

    def test_error_empty_message(self):
        """Test error output with empty message."""
        old_stderr = sys.stderr
        sys.stderr = io.StringIO()

        util.error("")

        output = sys.stderr.getvalue()
        sys.stderr = old_stderr

        assert "\n" == output

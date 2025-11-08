#!/usr/bin/env python
"""
Automated setup script for FastALPR with webcam support.
This script will install all required dependencies.
"""
import subprocess
import sys


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"► {description}")
    print(f"{'='*60}")
    print(f"Running: {command}\n")

    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            capture_output=True
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        print(f"✓ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} - FAILED")
        print(f"Error: {e.stderr}")
        return False


def main():
    """Main setup function."""
    print("""
╔═══════════════════════════════════════════════════════════╗
║         FastALPR Automated Setup Script                   ║
║         Installing dependencies...                        ║
╚═══════════════════════════════════════════════════════════╝
    """)

    # Check Python version
    print(f"Python version: {sys.version}")
    if sys.version_info < (3, 10):
        print("ERROR: Python 3.10 or higher is required!")
        sys.exit(1)

    steps = [
        (
            f'{sys.executable} -m pip install -e ".[onnx]"',
            "Installing FastALPR with ONNX runtime"
        ),
        (
            f'{sys.executable} -m pip uninstall opencv-python-headless -y',
            "Removing opencv-python-headless (no GUI support)"
        ),
        (
            f'{sys.executable} -m pip install opencv-python',
            "Installing opencv-python (with GUI support)"
        ),
    ]

    failed = []
    for command, description in steps:
        if not run_command(command, description):
            failed.append(description)

    # Summary
    print("\n" + "="*60)
    print("SETUP SUMMARY")
    print("="*60)

    if not failed:
        print("✓ All dependencies installed successfully!")
        print("\nNext steps:")
        print("  1. Test static image: python test_alpr.py")
        print("  2. Test webcam:       python test_webcam.py")
        print("  3. Run live ALPR:     python webcam_alpr.py")
        print("\nFor more info, see SETUP.md and WEBCAM_USAGE.md")
    else:
        print("✗ Some steps failed:")
        for step in failed:
            print(f"  - {step}")
        print("\nPlease check the errors above and try manual installation.")
        print("See SETUP.md for detailed instructions.")
        sys.exit(1)

    print("="*60)


if __name__ == "__main__":
    main()

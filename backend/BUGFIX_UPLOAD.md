"""
BUGFIX: File upload coroutine not being awaited
This file demonstrates the fix needed in router.py
"""

# OLD CODE (BROKEN):
# saved_path = save_upload_file(file)
# ext = saved_path.suffix.lower()  # ERROR: 'coroutine' has no attribute 'suffix'

# FIXED CODE:
# saved_path = await save_upload_file(file)
# ext = saved_path.suffix.lower()  # WORKS!

# The issue: save_upload_file is an async function but wasn't being awaited

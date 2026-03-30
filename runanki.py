#!/usr/bin/env python3
import os

import aqt

if not os.environ.get("ANKI_IMPORT_ONLY"):
    aqt.run()
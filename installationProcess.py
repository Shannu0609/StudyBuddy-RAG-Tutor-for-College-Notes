
    # ---------------------------------------------
    # print(f"Loaded documents: {len(documents)}")
    # print(f"Total text chunks: {len(text_chunks)}")

    # if text_chunks:
    #     print("\nFirst chunk preview:")
    #     print(text_chunks[0].page_content[:500])
    #     print("\nFirst chunk metadata:")
    #     print(text_chunks[0].metadata)
    # ------------------
    # print(f"Total pages loaded / files loaded : {len(documents)}")
    # print(documents[0].page_content)
    # for index , document in enumerate(documents , start = 1 ):

    #     print(f" {index} -> Document :")
    #     print(f"meta data: {document.metadata}")
    #     print(f"Page conent data: {document.page_content[:300]}")





# ============================================================
# SYSTEM DEPENDENCIES FOR UNSTRUCTURED PDF INGESTION
# ============================================================

# 1. POPPLER
# Purpose:
# - Provides PDF utilities such as pdfinfo and pdftoppm.
# - Helps inspect PDF page counts and convert PDF pages into images.
# - Required by pdf2image when Unstructured uses image-based PDF processing.
#
# Installation (Windows):
# - Download from:
#   https://github.com/oschwartz10612/poppler-windows/releases
# - Extract the downloaded ZIP to a permanent location, e.g.:
#   C:\poppler
# - Find the folder containing pdfinfo.exe and pdftoppm.exe.
#   It is usually a folder named "bin".
# - Add that folder to the Windows PATH environment variable.
# - Open a NEW terminal after updating PATH.
#
# Verification (PowerShell):
#   pdfinfo -v
#   pdftoppm -h
#
# IMPORTANT:
# - Installing the Python package pdf2image alone does NOT install Poppler.


# 2. TESSERACT OCR
# Purpose:
# - OCR stands for Optical Character Recognition.
# - Extracts text from scanned PDFs and images that contain text
#   as pixels rather than selectable text.
# - May be required when Unstructured processes image-based PDFs.
#
# Installation (Windows):
# - Download from:
#   https://github.com/UB-Mannheim/tesseract/wiki
# - Install Tesseract OCR.
# - Note the installation directory, commonly:
#   C:\Program Files\Tesseract-OCR
# - Add this directory to the Windows PATH environment variable.
# - Install the appropriate language data if needed.
# - Open a NEW terminal after updating PATH.
#
# Verification (PowerShell):
#   tesseract --version
#   tesseract --list-langs
#
# IMPORTANT:
# - Tesseract is an external application, not just a Python package.
# - Installing pytesseract alone does NOT install Tesseract OCR.
# - OCR is not necessary for every PDF; digitally generated PDFs
#   may contain extractable text without OCR.


# 3. PYTHON DEPENDENCIES
# Install these inside the activated project virtual environment:
#
#   python -m pip install "unstructured[pdf]"
#
# Check the installation:
#
#   python -m pip show unstructured
#   python -m pip show unstructured-inference
#
# IMPORTANT:
# - Poppler and Tesseract are system-level dependencies.
# - Unstructured and pdf2image are Python packages.
# - Keep the project virtual environment activated when installing
#   and running Python dependencies.


# 4. TROUBLESHOOTING
# - "PDFInfoNotInstalledError":
#   Check Poppler installation and PATH.
#
# - "tesseract is not installed or it's not in your PATH":
#   Check Tesseract installation and PATH.
#
# - If a command is not recognized:
#   Verify the executable's directory is in PATH and reopen the
#   terminal (or restart VS Code).
#
# - If PDF processing still fails:
#   Read the final exception in the traceback; other dependencies
#   or PDF-specific issues may also be responsible.
# ============================================================

# & "G:\RAG projects\Tools_tessract_proppler\proppler-26.09.0-0\poppler-26.09.0\Library\bin\pdfinfo.exe" -v


# $popplerPath = "G:\RAG projects\Tools_tessract_proppler\proppler-26.09.0-0\poppler-26.09.0\Library\bin"

# $userPath = [Environment]::GetEnvironmentVariable("Path", "User")

# if (($userPath -split ';') -notcontains $popplerPath) {
#     [Environment]::SetEnvironmentVariable(
#         "Path",
#         "$userPath;$popplerPath",
#         "User"
#     )
# }

# $env:Path += ";$popplerPath"


# & "C:\Program Files\Tesseract-OCR\tesseract.exe" --version


# $tesseractPath = "C:\Program Files\Tesseract-OCR"

# $userPath = [Environment]::GetEnvironmentVariable("Path", "User")

# if (($userPath -split ';') -notcontains $tesseractPath) {
#     [Environment]::SetEnvironmentVariable(
#         "Path",
#         "$userPath;$tesseractPath",
#         "User"
#     )
# }

# $env:Path += ";$tesseractPath"
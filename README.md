# VoterIdTextExtractor

extract essential info from image of voter Id using opencv+PIL+pytesseract

# Instructions

- Install pytesseract

        pip install pytesseract

- Install binaries for pytesseract by running tesseract-ocr-w64-setup-v5.0.0-alpha.20200328.exe file

- set tesseract.exe file install location

        pytesseract.pytesseract.tesseract_cmd = r'E:\Tesseract-OCR\tesseract'(set like yours)

* set TESSDATA_PREFIX environment by giving tessdata folder path

        TESSDATA_PREFIX=r'E:\Tesseract-OCR\tessdata' (set like yours)

* Running the extractor

        python extractcli.py --img front_image.jpg back_image.jpg

It will print the extracted info in the cmd.

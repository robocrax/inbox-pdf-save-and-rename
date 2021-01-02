# Bulk save PDF's from Gmail and rename
Using Google Apps Script (free quota) for any incoming mails with matching params and PDF attachment, saves it and optionally renames it by converting PDF to text using OCR and using content in it.

Email is marked as read after script downloads the email to notify user/you. Can also add a label once done if you prefer

## For printing

Additionally to automatically print the attachments, I'm using [benjamin-kromer](https://github.com/benjamin-kromer)'s [printHotfolder](https://github.com/benjamin-kromer/printHotfolder) python script: https://github.com/benjamin-kromer/printHotfolder/blob/master/printHotfolder.py but using Python 3

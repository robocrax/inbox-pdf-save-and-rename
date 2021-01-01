/*
 *) Note:
 * Depreciated this in favour of SHARP auto-email forwarding then printing
 * Kinda efficient and cheaper then script runtime limitations
 * 
 *) Note 2:
 * Back in action. Attempting to create open source PDF file renamer from content inside
 *
 *) Note 3:
 * fkn ditch Python the app and use Google Scripts. Thanks Google!
 * Google execution notice/warning: It takes 3 times longer than downloading just to get a new name from content
 * 
 *              1x             +       3x         =          4x
 *     download attachment           rename              new runtime
 *
 */








// VARS


// Query (similar within GMail search) to search for these emails throughout the entirety of GMail
const query = ' in:inbox is:unread from:(organization.co.nz OR someone@yahoo.co.nz) subject:(purchase order) filename:pdf '

// ID of the folder in google drive in which files are
const folderID = '1qwfeeyOdnAFpblxq8OGgyHe93K_Q2Pp293';

const regex_separator = '_';
const regex_finds = {
  "contact": "Contact: ([^\s]+)",                     // First word 
  "deliver_to": "Deliver to: ([A-Z]{4})",             // slide those 4 digits
  "rebel_po": "PO Number: (\d{10})",                  // 10 digits
  "order_date": "Order Date: (\d{2}.\d{2}.\d{4})",    // The periods (fullstops) stand for any character, not the literal dot.
};

const matchName = "Purchase Order.pdf";

















/*########################################################
* It is what it is
*
* Made and adjusted earlier so no description.
*
*/
function GmailToDrive() {
  //build query to search emails
  var threads = GmailApp.search(query);
  //var label = getGmailLabel_(labelName);
  var parentFolder;
  if (threads.length > 0) {
    parentFolder = DriveApp.getFolderById(folderID);
  }
  for (var i in threads) {
    var mesgs = threads[i].getMessages();
    for (var j in mesgs) {
      //get attachments
      var attachments = mesgs[j].getAttachments();
      for (var k in attachments) {
        var attachment = attachments[k];
        var attachmentBlob = attachment.copyBlob();

        var gdriveFolder = DriveApp.getFolderById(folderID);
        let fileID = gdriveFolder.createFile(attachmentBlob).getId();
        let file = DriveApp.getFileById(fileID)

        // Rename file if it matches this name:
        if (file.getName() == matchName) {
          new_name = getNameFromContent(file);
          Logger.log("Saved " + file.setName(new_name + '.pdf'));   // since output of setName is exactly the new setName, 1-liner baby
        }
      }

      // Mark attachment as read
      GmailApp.markMessageRead(mesgs[j]);
    }
    //threads[i].addLabel(label);
  }
}

/*########################################################
* The renamer... Uses OCR function and Regex function 
*
* param {string} : obj : DriveApp.file of the PDF that the text will be extracted from.
*
* returns new_name : generated using regex values and separator
*
*/
function getNameFromContent(file) {

  // Get text using Drive 2.0 OCR
  const content = getTextFromPDF(file);

  var new_name = '';
  var regex_found = {};

  for (find in regex_finds) {
    if (new_name !== '') {
      new_name += regex_separator; // lamest way to add a separator, and I have an account in leetcode
    }

    let found = extractUsingRegex(content, regex_finds[find]);
    regex_found[find] = found;

    // temp replace rebel contact because numbers regex is not working
    if (find === "contact") {
      found = found.split(" ")[0];
      regex_found["contact"] = found;
    }

    new_name += found;
  }

  return new_name;

};

/*########################################################
* Extracts the text from a PDF and stores it in memory.
*
* param {string} : file : file ID of the PDF that the text will be extracted from.
*
* returns text : Contains the PDF text.
*
*/
function getTextFromPDF(file) {
  var blob = file.getBlob()
  var resource = {
    title: blob.getName(),
    mimeType: blob.getContentType()
  };
  var options = {
    ocr: true,
    ocrLanguage: "en"
  };
  // Convert the pdf to a Google Doc with ocr.
  var file = Drive.Files.insert(resource, blob, options);

  // Get the texts from the newly created text.
  var doc = DocumentApp.openById(file.id);
  var text = doc.getBody().getText();

  // Deleted the temporary OCR document once the text has been stored to var.
  Drive.Files.remove(doc.getId());

  return text;
}

/*########################################################
* Use the text extracted from PDF and extracts content (via given regex)
*
* param {string} : str : text of data from PDF.
* param {string} : look_for : regex expression with 1 matching group which is the content that will be returned. 
*                             Use https://regex101.com/ to understand what you probably need.
*
* returns {array} : str : containing contents in the first matching group
*
*/
function extractUsingRegex(str, look_for) {
  try {
    let found = str.match(look_for);
    return found[1];                   // Like $1 match group (fixed for this script)
  } catch (e) {
    let found = "error";
    return found;
  }
};

/*########################################################
* Unused function. In case at any point in future you already have a few PO's in your drive, then process those manually (once) here
*
* required {string} : folderID in which the PDF files are stored.
*
* returns nothing
*
*/
function manualRenameFromFolder() {

  //Get all PDF files (not necessarily named "New Purchase Order Printout.pdf")
  const folder = DriveApp.getFolderById(folderID);
  //const files = folder.getFiles();
  const files = folder.getFilesByType("application/pdf");

  //Iterate through each folderr
  while (files.hasNext()) {
    let file = files.next();

    // Get new name using regex function
    new_name = getNameFromContent(file);

    // Rename and log
    Logger.log("Renamed " + file.setName(new_name + '.pdf') + " from " + folder.getName());   // since output of setName is exactly the new setName, 1-liner baby
  }
  
};

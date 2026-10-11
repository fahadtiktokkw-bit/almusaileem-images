/**
 * Almusaileem Project Intake V6 - Google Apps Script.
 * Deploy manually as a Web App after reviewing access settings.
 * Script Properties: INTAKE_TOKEN (random secret), SHEET_ID (Google Sheet ID).
 * This endpoint is NOT deployed by publishing this file.
 */
const FIELDS = ['name','phone','area','service','notes'];
function clean(value, limit) {
  const s = String(value == null ? '' : value).trim().slice(0, limit);
  return /^[=+@\-]/.test(s) ? "'" + s : s;
}
function doPost(e) {
  try {
    if (!e || !e.postData || !e.postData.contents) throw Error('Missing request');
    const data = JSON.parse(e.postData.contents);
    const props = PropertiesService.getScriptProperties();
    const secret = props.getProperty('INTAKE_TOKEN');
    const sheetId = props.getProperty('SHEET_ID');
    if (!secret || !sheetId) throw Error('Not configured');
    if (String(data.token || '') !== secret) throw Error('Unauthorized');
    const name = clean(data.name,100), phone = String(data.phone || '').replace(/[^0-9]/g,'');
    if (!name || !/^(?:965)?[0-9]{8}$/.test(phone)) throw Error('Invalid name or phone');
    const lock = LockService.getScriptLock();
    lock.waitLock(10000);
    try {
      const sheet = SpreadsheetApp.openById(sheetId).getSheetByName('المشاريع');
      if (!sheet) throw Error('Projects sheet not found');
      const id = 'ALM-' + Utilities.formatDate(new Date(), 'Asia/Kuwait','yyyyMMdd-HHmmss') + '-' + Math.floor(Math.random()*9000+1000);
      const row = new Array(26).fill('');
      row[0]=id; row[1]=new Date(); row[2]=name; row[3]=phone;
      row[4]=clean(data.area,100); row[5]=clean(data.service || 'مايكروسمنت',100);
      row[13]='بانتظار الصور'; row[20]='غير معتمد'; row[24]=clean(data.notes,1000); row[25]=new Date();
      sheet.appendRow(row);
      const r=sheet.getLastRow();
      sheet.getRange(r,10).setFormula('=IF(COUNT(G'+r+':I'+r+')<3,"",G'+r+'*H'+r+')');
      sheet.getRange(r,11).setFormula('=IF(COUNT(G'+r+':I'+r+')<3,"",2*(G'+r+'+H'+r+')*I'+r+')');
      sheet.getRange(r,13).setFormula('=IF(OR(J'+r+'="",K'+r+'=""),"",J'+r+'+K'+r+'-IF(L'+r+'="",0,L'+r+'))');
      sheet.getRange(r,20).setFormula('=IF(OR(M'+r+'="",R'+r+'=""),"",M'+r+'*R'+r+'+IF(S'+r+'="",0,S'+r+'))');
      return ContentService.createTextOutput(JSON.stringify({ok:true,project_id:id})).setMimeType(ContentService.MimeType.JSON);
    } finally { lock.releaseLock(); }
  } catch(err) {
    return ContentService.createTextOutput(JSON.stringify({ok:false,error:String(err.message)})).setMimeType(ContentService.MimeType.JSON);
  }
}

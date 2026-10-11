# Almusaileem Project Intake V6
This Google Apps Script receives project intake submissions and appends them to the existing Google Sheet.

## Status
Source code only. NOT deployed. No public URL or WhatsApp integration is active.

## Deployment
1. Open the projects Google Sheet and select Extensions > Apps Script.
2. Paste the content of `apps_script_intake.gs`.
3. In Script Properties, set `SHEET_ID` to the spreadsheet ID and `INTAKE_TOKEN` to a long random secret.
4. Review privacy and access permissions. A public "Anyone" web app should not be enabled without additional authentication, anti-abuse controls, and customer privacy review.
5. Deploy as Web App using an access policy appropriate to your organization.
6. Send a JSON POST with `token`, `name`, `phone`, `area`, `service`, and `notes`. Do not put the token in a public web page.
7. Verify that the row appears in the المشاريع tab and dashboard updates.

Spreadsheet: https://docs.google.com/spreadsheets/d/1pENZdFhL2MfEoxiTVKMV11KdnYi6eDWyywS7Nk4igas/edit

## Limits
Apps Script Web App response does not set a custom HTTP error status; check the `ok` field. The example uses a shared token and is appropriate only for a trusted server-side sender, not a public browser form. No automatic WhatsApp messages are sent. User must explicitly authorize deployment.

from dotenv import load_dotenv
from smtp.mail_sender import send_email
import os 

load_dotenv()

PRODUCTION = os.getenv("PRODUCTION", "FALSE").upper() == "TRUE"

def sende_lieferverzugs_mail(empfaenger_email, bestellnummer, voraussichtliche_kw, komission, artikelbeschreibung):
    if not PRODUCTION:
        print(f"Sending email to {empfaenger_email} regarding order {bestellnummer} with new delivery week {voraussichtliche_kw}")
    to_adress = empfaenger_email if PRODUCTION else "konfigurator@rehatec.com"
    send_email(
        to_address=to_adress,
        subject=f"Aktualisierung zu Ihrem Auftrag {bestellnummer}",
        html_body = f"""
<p>Sehr geehrte Damen und Herren,</p>

<p>hiermit informieren wir Sie über den aktuellen Stand Ihres Auftrags:</p>

<p><b>Auftragsnummer:</b> {bestellnummer}<br>
<b>Kommission:</b> {komission}<br>
<b>Produkt</b>: {artikelbeschreibung}</p>

<p>Der Versand Ihres Auftrags wurde geändert und ist nun für Kalenderwoche <b>{voraussichtliche_kw}</b> vorgesehen.</p>

<p>Sollten sich weitere Änderungen ergeben, informieren wir Sie selbstverständlich zeitnah.</p>

<p>Vielen Dank für Ihr Vertrauen. Bei Fragen zu Ihrem Auftrag steht Ihnen unser Team gerne zur Verfügung.</p>

<p>Mit freundlichen Grüßen<br><br>
Ihr Rehatec GmbH - Team</p>
"""
    )

if __name__ == "__main__":
    sende_lieferverzugs_mail("konfigurator@rehatec.com", "AU202607-12345", "12", "34")
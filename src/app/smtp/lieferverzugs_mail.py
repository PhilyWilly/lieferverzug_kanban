from smtp.mail_sender import send_email

def sende_lieferverzugs_mail(empfaenger_email, bestellnummer, voraussichtliche_kw, komission):
    send_email(
        to_address="konfigurator@rehatec.com", # TODO: Replace with empfaenger_email when ready
        subject=f"Aktualisierung zu Ihrem Auftrag {bestellnummer}",
        html_body = f"""
<p>Sehr geehrte Damen und Herren,</p>

<p>wir möchten Sie über den aktuellen Stand Ihres Auftrags informieren:</p>

<p><b>Auftragsnummer:</b> {bestellnummer}<br>
<b>Kommission:</b> {komission}</p>

<p>Der Versand Ihres Auftrags ist aktuell für die Kalenderwoche {voraussichtliche_kw} vorgesehen.</p>

<p>Über Änderungen des Versandtermins informieren wir Sie selbstverständlich zeitnah.</p>

<p>Vielen Dank für Ihr Vertrauen. Bei Fragen zu Ihrem Auftrag steht Ihnen unser Team gerne zur Verfügung.</p>

<p>Mit freundlichen Grüßen<br><br>
Ihr Rehatec GmbH - Team</p>
"""
    )

if __name__ == "__main__":
    sende_lieferverzugs_mail("konfigurator@rehatec.com", "AU202607-12345", "12", "34")
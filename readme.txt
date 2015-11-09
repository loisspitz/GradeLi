GradeLi Ver. 1.0
Autor: Holger Trampe
www.holgertrampe.de
Lizenz: CC 2.0 (Autor benennen! Verändern, Entwickeln aber NICHT VERKAUFEN oder in Teilen für kostenpflichtige Sftware einsetzen! GradeLi ist und bleibt OpenSource!)

Installation

1. GradeLi-Ordner in ein Cloudfähiges Verzeichnis verschieben (wenn Synchrosiation erwünscht ist, ansonsten in ein Verzeichnis mit Schreibrechten (z.B. home/IHRBENUTZERNAME/)
2. Die Desktop-Datei in .local/share/applications verschieben und ggf. anpassen
3. Programm starten mit "GradeLi_Start.py"

Benötigte Pakete:

python-tk (installation Ubuntu: sudo apt-get install python-tk)

Benutzung

GradeLi erstellt beim ersten Start den Ordner "GradeLi Classes" im gleichen Verzeichnis. Hier werden später ALLE KLASSENDATEN gespeichert. Man kann das Programm (welches im Ordner GradeLi ist) also ohne Datenverlust aktualisieren.

Erster Start

Beim ersten Start wird eine Warnmeldung ausgegeben, dass ein Ordner "GradeLi Classes" erstellt, aber keine Klassen gefunden wurden.
Erstellen Sie anschließend einfach eine neue Klasse. Geben Sie einen Aussagekräftigen Namen ein (vermeiden Sie Sonderzeichen!).

Nachdem Sie eine Klasse erstellt haben können Sie manuel oder per Import einer CSV-Datei Schüler importieren.
CSV-Format:
Vorname, Nachname, E-Mailadresse

Wird keine E-Mailadresse gespeichert den Teil leer lassen. Beispiel:

Holger,Trampe,mail@holgertrampe.de
Johannes,Marks,
Sabrina,Schalda,sschalda@mailme.com

Einheiten

Erstellen Sie Einheiten (Datum und wahlweise einen Titel) unter "Einheiten". Dort können Sie folgende Daten speichern:
Fragezeichen	Schüler unentschuldigt gefehlt
Daumen Hoch 	Schüler entschuldigt gefehlt
Schulbus	Schüler war auf einer internen Schuleveranstaltung o.ä.
+/-		Schüler hat in dieser Stunde eine mittelmäßige Leistung erbracht
++/+		Positive Mitarbeit in zwei Stufen
--/.		Negative Mitarbeit in zwei Stufen

Noten

In GradeLi können Sie umfangreiche Notensystem erstellen. Das System gliedert sich in Ober- und Unterkategorien.
Beispiel:

Oberkategorie Schriftlich (Gewichtung 70) und Mündlich (30). Für diese Oberkategorien können nun Unterkategorien angelegt werden (z.B. 
ein Vortrag, welcher sich dann in zwei Noten (z.B. Handout und Vortragsstil) gliedert. Diese Noten können entsprechend unterschiedliche
gewichtet werden). Das Program berechnet anschließend alle Noten entsprechend ihrer Gewichtung. Das Ergebnis kann unter "Einzelansicht" 
betrachtet werden.

Gesamtübersicht

Hier werden alle Daten gesammelt angezeigt, um einen schnellen Überblick zu erhalten.

Sollten Sie Fragen, Wünsche oder einen Fehler gefunden haben senden Sie eine Mail an mail@holgertrampe.de

SOURCE ICONS: www.flaticon.com Lizenz CC BY 3.0 Creative Commons

GradeLi ist eine freie Software und darf weiterentwickelt werden. Bitte immer den Autor benennen!

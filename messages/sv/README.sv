I allm�nhet beh�ver du g�ra tv� saker f�r att l�gga till �vers�ttningar 
f�r ett spr�k i Mailman. Du m�ste �vers�tta meddelandekatalogen och du 
m�ste �vers�tta mallarna.

F�r att �vers�tta meddelandekatalogen g�r du en kopia av filen 
/messages/mailman.pot. Kopian d�per du till mailman.po och l�gger
i underkatalogen messages/xx/LC_MESSAGES. Sen redigerar du filen och 
l�gger till �vers�ttningarna f�r varje meddelande som finns i katalogen.
Att ha ett bra verktyg i denna del av arbetet �r en god hj�lp, till exempel 
po-mode for Emacs.

N�r du lagt till dina �vers�ttningar, kan du k�ra msgfmt via din .po-fil 
f�r att generera messages/xx/LC_MESSAGE/mailman.mo.

N�sta steg �r att skapa underkatalogen templates/xx och �vers�tta alla
filerna i templates/en/*.{html,txt}. Dessa b�r du ocks� �terf�ra till
Mailman-projektet.

F�r att uppm�rksamma Mailman och dina listor p� det nya spr�ket, f�ljer du 
direktiven i avsnittet ovan.

�VERS�TTNINGSTIPS
 	Fr�ga: Hur ska bokst�ver och tecken som inte ing�r i ASCII-alfabetet, 
	till exempel franskans cedilj, hanteras i kataloger och mallar?

	Svar: Alla meddelanden som �r avsedda f�r att visas p� webben
	kan inneh�lla en begreppsh�nvisning i HTML n�r det
	beh�vs. Meddelanden som �r avsedda f�r e-post b�r uttryckligen
	anv�nda specialtecken utanf�r ASCII-alfabetet. Detta g�ller
	f�r b�de meddelandekatalogen och mallarna.

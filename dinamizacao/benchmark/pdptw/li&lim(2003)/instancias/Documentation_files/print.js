function printPage() {
	var da = (document.all) ? 1 : 0;
	var pr = (window.print) ? 1 : 0;

	if (!pr)
		return;

var printArea = document.getElementById("ContainerDiv");

	if (printArea == null && da)
		printArea = document.all.MainAreaDiv;

	if (printArea) {
	    var sStart = "<html><head><link rel=\"stylesheet\" type=\"text/css\" href=\"/styles/WebForms/structure.css\"><link rel=\"stylesheet\" type=\"text/css\" href=\"/styles/WebForms/searchBox.css\"><link rel=\"stylesheet\" type=\"text/css\" href=\"/styles/WebForms/predefinertsok.css\"><link rel=\"stylesheet\" type=\"text/css\" href=\"/Styles/editor.css\"><link rel=\"stylesheet\" type=\"text/css\" href=\"/Styles/units.css\"><link rel=\"stylesheet\" type=\"text/css\" href=\"/Styles/Resources/print.css\"></head><body onload=\"javascript:window.print();\">";
		sStop = "</body></html>";

		var w = window.open('about:blank', 'printWin', 'width=650,height=440,scrollbars=yes');
		wdoc = w.document;
		wdoc.open();
		wdoc.write(sStart + printArea.innerHTML);
		wdoc.writeln(sStop);
		setTimeout(function() { wdoc.close(); }, 1000); /* IE..-9 bug krever at man venter i 1000ms før document lukkes */
		
	}
}
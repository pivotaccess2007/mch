		function start() {
				myform.ca.checked = false;
				myform.cb.checked = false;
				myform.cc.checked = false;
				myform.cd.checked = false;
				myform.provchoose.disabled = true;
				myform.distchoose.disabled = true;
				myform.hdchoose.disabled = true;
				myform.locchoose.disabled = true;
				}
				onload = start;
				function chgtx() {
					myform.provchoose.disabled = !myform.ca.checked;
					}
				function chgty() {
					myform.distchoose.disabled = !myform.cb.checked;
					}
				function chgtz() {
					myform.hdchoose.disabled = !myform.cc.checked;
					}
				function chgtv() {
					myform.locchoose.disabled = !myform.cd .checked;
					}
				
				

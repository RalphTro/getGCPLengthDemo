$(document).ready(function () {
	// when document loaded:

	// Function to fetch the date of this tool's GCP JSON file
	$.getJSON('gcp_data/gcpprefixformatlist.json', function (gs1Data) {
		var fullDate = new Date(gs1Data.GCPPrefixFormatList.date);
		var options = { day: 'numeric', month: 'long', year: 'numeric' };
		var date = fullDate.toLocaleDateString('en-GB', options).replace(/,/g, '');
		// console.log(date);
		$("#gs1-updated").html(date);
	});

	// Function to fetch the date of the date when GS1's global GCP length table was updated
	// NOTE: to prevent that the JSON file (Jan 2025: > 15 MB) itself must be loaded for this purpose, we only extract it from GS1's landing page 
	$.ajax({
		url: "https://api.allorigins.win/get?url=" + encodeURIComponent("https://www.gs1.org/standards/bc-epc-interop"),
		success: function (response) {
			var data = $(response.contents);
			var date = data.find("#block-gsone-revamp-content .content article .bg-white .container .layout .col-md-12 .block .content div[property='schema:text'] p:contains('Updated') strong font i").text();
			// console.log("Updated Date: " + date);
			$("#global-gcp-date").html(date);
		}
	});

	// Regular expressions for GS1 keys
	const gs1KeyRegEx = {
		'00': /^(\d{18})$/,
		'01': /^(\d{14})$/,
		'253': /^(\d{13})([\x21-\x22\x25-\x2F\x30-\x39\x3A-\x3F\x41-\x5A\x5F\x61-\x7A]{0,17})$/,
		'255': /^(\d{13})(\d{0,12})$/,
		'401': /^([\x21-\x22\x25-\x2F\x30-\x39\x3A-\x3F\x41-\x5A\x5F\x61-\x7A]{0,30})$/,
		'402': /^(\d{17})$/,
		'414': /^(\d{13})$/,
		'417': /^(\d{13})$/,
		'8003': /^(\d{14})([\x21-\x22\x25-\x2F\x30-\x39\x3A-\x3F\x41-\x5A\x5F\x61-\x7A]{0,16})$/,
		'8004': /^([\x21-\x22\x25-\x2F\x30-\x39\x3A-\x3F\x41-\x5A\x5F\x61-\x7A]{0,30})$/,
		'8006': /^(\d{14})(\d{2})(\d{2})$/,
		'8010': /^([\x23\x2D\x2F\x30-\x39\x41-\x5A]{0,30})$/,
		'8017': /^(\d{18})$/,
		'8018': /^(\d{18})$/
	};

	// Key starts with GCP
	const keyStartsWithGCP = {
		'00': false,
		'01': false,
		'253': true,
		'255': true,
		'401': true,
		'402': true,
		'414': true,
		'417': true,
		'8003': false,
		'8004': true,
		'8006': false,
		'8010': true,
		'8017': true,
		'8018': true
	};

	function getGCPLength(aI, gs1Key) {
		try {
			// Check if GS1 Key complies with its corresponding RegEx
			if (!gs1KeyRegEx[aI].test(gs1Key)) {
				throw new Error('The GS1 Key has an incorrect length or impermissible characters.');
			}
		} catch (error) {
			return error.message;
		}

		// Variables storing identified gcp length and specifying prefix length/search string
		let gcpLength = "";
		let j = 12;

		// Normalize leading zero so that function works consistently for all GS1 keys
		if (keyStartsWithGCP[aI]) {
			gs1Key = '0' + gs1Key;
		}
		//console.log('gs1Key: ', gs1Key);

		// Normalize further by removing any characters after a non-numeric character appears, if present
		let firstNonNumericIndex = gs1Key.search(/\D/);
		// console.log('firstNonNumericIndex', firstNonNumericIndex)
		if (firstNonNumericIndex !== -1) {
			gs1Key = gs1Key.substring(0, firstNonNumericIndex);
		}

		// Check if there are matching 12-digit prefix values.
		// If not, iterate further (i.e. decrease GCP length) until there is a match.
		// Then, return corresponding GCP Length Value
		while (j > 2 && !gcpLength) {
			for (let i = 0; i < gcpDict.length; i++) {
				if (gcpDict[i].prefix.length === j && gs1Key.substring(1, j + 1).includes(gcpDict[i].prefix)) {
					gcpLength = gcpDict[i].gcpLength;
					return gcpLength;
				}
			}
			j -= 1;
		}

		if (!gcpLength) {
			throw new Error('No matching value. Try Verified by GS1 (https://www.gs1.org/services/verified-by-gs1) or contact your local GS1 MO.');
		}
	}

	// Load GCP Length Table data from local JSON file
	fetch('gcp_data/gcpprefixformatlist.json')
		.then(response => response.json())
		.then(allGCPs => {
			// Transform JSON structure into list of dictionaries
			gcpDict = allGCPs.GCPPrefixFormatList.entry;

		})
		.catch(error => console.error('Error loading JSON file:', error));

	$("#get-gcp").on("click", function () {
		// console.log(getGCPLength($("#dropdown").val(), $("#input").val()))
		try {
			$("#output").html(getGCPLength($("#dropdown").val(), $("#input").val()).toString());
		} catch (error) {
			$("#output").html(error.message);
		}
	});

	$("#clear").on("mousedown", function () {
		$("#dropdown").val('');
		$("#input").val('');
		$("#output").html('');
	});

	$("#gtin").on("click", function () {
		$("#input").val('04150999999994');
		$("#dropdown").val('01');
	});

	$("#sscc").on("click", function () {
		$("#input").val('340123453111111115');
		$("#dropdown").val('00');
	});

	$("#gln").on("click", function () {
		$("#input").val('4280000000002');
		$("#dropdown").val('417');
	});

	$("#giai").on("click", function () {
		$("#input").val('425121832999XYZ');
		$("#dropdown").val('8004');
	});

	$("#grai").on("click", function () {
		$("#input").val('03870585000552987');
		$("#dropdown").val('8003');
	});

	$("#itip").on("click", function () {
		$("#input").val('095211411234540102');
		$("#dropdown").val('8006');
	});

	$(".demo-button, #clear, #get-gcp").hover(
		function () {
			$(this).css("cursor", "pointer");
		},
		function () {
			$(this).css("cursor", "default");
		}
	);

});

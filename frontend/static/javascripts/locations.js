	
				
				//START FILTERING LOCATIONS
				var provinces = [];
				var districts = [];
				var locations = [];
				var villages   = [];
				var hps = [];
				var sectors = [];
				var cells = [];
				var villages = [];
				var url  = document.URL.split("?");
				var url2 = "";
				if (url.length > 1) url2 = url[1];

				sel_prov = getQueryParameter ( "province" );
				sel_dist = getQueryParameter ( "district" );
				sel_hd = getQueryParameter ( "hd" );
				sel_loc = getQueryParameter ( "hc" );

				$.getJSON( "/locs?"+url2 , function( result ){
				
						provinces = _.map(_.indexBy(result['hcs'], 'province_pk'), function(obj){return obj});
						districts = _.map(_.indexBy(result['hcs'], 'district_pk'), function(obj){ return obj });
						hps = _.map(_.indexBy(result['hcs'], 'referral_facility_pk'), function(obj){ return obj });
						//alert(hps);
						locations = result['hcs'];
						sectors = _.map(_.indexBy(result['villages'], 'sector_pk'), function(obj){return obj});
						cells = _.map(_.indexBy(result['villages'], 'cell_pk'), function(obj){return obj});
						villages = result['villages'];

						//alert( sel_prov+ ", "+ sel_dist + ", " + sel_loc );
				if (sel_prov == '' || sel_prov == undefined || sel_prov == null) sel_prov = getQueryParameter ( "province" );
				if (sel_dist == '' || sel_dist == undefined || sel_dist == null) sel_dist = getQueryParameter ( "district" );

				if (sel_hd == '' || sel_hd == undefined || sel_hd == null) sel_hd = getQueryParameter ( "hd" );
				if (sel_loc == '' || sel_loc == undefined || sel_loc == null) sel_loc = getQueryParameter ( "hc" );
					
						//alert( provinces.length+ ", "+ districts.length + ", " + locations.length );
						
						document.getElementById('provchoose').options.length = provinces.length + 1;
						document.getElementById('provchoose').options[0] = new Option("Select Province", "");

						document.getElementById('distchoose').options.length = districts.length +1 ;
						document.getElementById('distchoose').options[0] = new Option("Select District", "");
			
						document.getElementById('hdchoose').options.length = hps.length +1 ;
						document.getElementById('hdchoose').options[0] = new Option("Select Hospital", "");

						document.getElementById('locchoose').options.length = locations.length + 1;
						document.getElementById('locchoose').options[0] = new Option("Select Health Centre", "");

						for ( var i=0; i<provinces.length; i++ ){
							province = provinces[i]							
							document.getElementById('provchoose').options[i+1] = new Option(province.province_name, province.province_pk);
 							
							}

						for ( var i=0; i<districts.length; i++ ){
							district = districts[i]
							document.getElementById('distchoose').options[i+1] = new Option(district.district_name, district.district_pk);
								}

						for ( var i=0; i<hps.length; i++ ){
							hd = hps[i]
							document.getElementById('hdchoose').options[i+1] = new Option(hd.referral_name, hd.referral_facility_pk);
								}
					
						for ( var i=0; i<locations.length; i++ ){
								hc = locations[i]
								document.getElementById('locchoose').options[i+1] = new Option(hc.name, hc.indexcol);
								}

						if (sel_prov != '' ){
							 prv_index = fetch_index_from_option_value(document.getElementById('provchoose').options, sel_prov);
							 document.getElementById('provchoose').options[prv_index].selected = true;
							 changeDistrict(sel_prov);							 
							     }	
	
						if (sel_prov != '' && sel_dist != '') {
								dist_index = fetch_index_from_option_value(document.getElementById('distchoose').options, sel_dist);
							 	document.getElementById('distchoose').options[dist_index].selected = true;
								changeHospital(sel_dist);
									}

						if (sel_hd != '' && sel_dist != '') {
								hd_index = fetch_index_from_option_value(document.getElementById('hdchoose').options, sel_hd);
							 	document.getElementById('hdchoose').options[hd_index].selected = true;
								changeLocation(sel_hd);
									}

						if (sel_loc != '' && sel_hd != '') { 									
								loc_index = fetch_index_from_option_value(document.getElementById('locchoose').options, sel_loc);
							 	document.getElementById('locchoose').options[loc_index].selected = true;
								}				
				
	    					});
					
				function fetch_index_from_option_value(options, value){ 
											for(i=0;i<options.length;i++) 
											{ 
											if(options[i].value == value) break; 
											
											 }
											
											return i
											}

				function changeDistrict(value){

					var selected_districts = _.filter(districts, function(item) {  return item.province_pk == value;  });
					document.getElementById('distchoose').options.length = selected_districts.length + 1;
					document.getElementById('distchoose').options[0] = new Option("Select District", "");
					for ( var i=0; i<selected_districts.length; i++ ){
							district = selected_districts[i]
							document.getElementById('distchoose').options[i+1] = new Option(district.district_name, district.district_pk);
								}
					/*
					sel_prov = document.getElementById('provchoose').value;
					sel_dist = document.getElementById('distchoose').value;
					sel_loc  = document.getElementById('locchoose').value; 
					
					prv_index = fetch_index_from_option_value(document.getElementById('provchoose').options, sel_prov);
					if( prv_index != '') document.getElementById('provchoose').options[prv_index].selected = true;
					dist_index = fetch_index_from_option_value(document.getElementById('distchoose').options, sel_dist);
					if( dist_index != '') document.getElementById('distchoose').options[dist_index].selected = true;				
					loc_index = fetch_index_from_option_value(document.getElementById('locchoose').options, sel_loc);
				 	if( loc_index != '') document.getElementById('locchoose').options[loc_index].selected = true;
					*/
					}


				function changeHospital(value){
					//alert("change Hospital:" + value);
					var selected_hps = _.filter(hps, function(item) {  return item.district_pk == value; });
					document.getElementById('hdchoose').options.length = selected_hps.length + 1;
					document.getElementById('hdchoose').options[0] = new Option("Select Hospital", "");
											
					for ( var i=0; i<selected_hps.length; i++ ){
								hp = selected_hps[i];
							//alert("HP: " + hp.referral_name + ", " + hp.referral_facility_pk);
							document.getElementById('hdchoose').options[i+1] = new Option(
														hp.referral_name,
														 hp.referral_facility_pk);
								}
					}


				function changeLocation(value){

					var selected_locations = _.filter(locations, function(item) { 
												return item.referral_facility_pk == value; });
					document.getElementById('locchoose').options.length = selected_locations.length + 1;
					document.getElementById('locchoose').options[0] = new Option("Select Health Centre", "");
											
					for ( var i=0; i<selected_locations.length; i++ ){
								hc = selected_locations[i]
								document.getElementById('locchoose').options[i+1] = new Option(hc.name, hc.indexcol);
								}
					/*
					sel_prov = document.getElementById('provchoose').value;
					sel_dist = document.getElementById('distchoose').value;
					sel_loc  = document.getElementById('locchoose').value; 
					dist_index = fetch_index_from_option_value(document.getElementById('distchoose').options, sel_dist);
					if( dist_index != '') document.getElementById('distchoose').options[dist_index].selected = true;				
					loc_index = fetch_index_from_option_value(document.getElementById('locchoose').options, sel_loc);
				 	if( loc_index != '') document.getElementById('locchoose').options[loc_index].selected = true;
					*/
					}

				function changeSector(value){
					
					var selected_cells = _.filter(cells, function(item) {  return item.sector_id == value;  });

					for ( var i=0; i<selected_cells.length; i++ ){
								cell = selected_cells[i]
								document.getElementById('cellchoose').options.length = selected_cells.length;
								document.getElementById('cellchoose').options[i] = new Option(cell.cell_name, cell.cell_id);
								}
						document.getElementById('cellchoose').options[selected_cells.length] = new Option("Cell", "");
						document.getElementById("cellchoose").selectedIndex = selected_cells.length;
					}


			       function changeCell(value){

					var selected_villages = _.filter(villages, function(item) {  return item.cell_id == value;  });
			
					for ( var i=0; i<selected_villages.length; i++ ){
								village = selected_villages[i]
								document.getElementById('villchoose').options.length = selected_villages.length;
								document.getElementById('villchoose').options[i] = new Option(village.name, village.id);
								}
						document.getElementById('villchoose').options[selected_villages.length] = new Option("Village", "");
						document.getElementById("villchoose").selectedIndex = selected_villages.length;
					}
				
				function PassCheck(filter_form){
					
						// FIX CASES YOU CAN FORGET TO DISABLE SOME FILTERS AND THEY ARE EMPTY ... 
						if(filter_form.provchoose.value == ""){
											filter_form.provchoose.disabled = true;
											}
						else if(filter_form.distchoose.value == ""){
											filter_form.distchoose.disabled = true;
											}
						else if(filter_form.hdchoose.value == ""){
											filter_form.hdchoose.disabled = true;
											}
						else if(filter_form.locchoose.value==""){
											filter_form.locchoose.disabled = true;
										}

						filter_form.submit();

					}

				function getQueryParameter ( parameterName ) {

						  var queryString = window.top.location.search.substring(1);
						  var parameterName = parameterName + "=";
						  if ( queryString.length > 0 ) {
						    begin = queryString.indexOf ( parameterName );
						    if ( begin != -1 ) {
						      begin += parameterName.length;
						      end = queryString.indexOf ( "&" , begin );
							if ( end == -1 ) {
							end = queryString.length
						      }
						      return unescape ( queryString.substring ( begin, end ) );
						    }
						  }
						  return "";

						} 
				function make_location_of_parent(name, url){
						var prv = getQueryParameter ( "province" );
						var dst = getQueryParameter ( "district" );
						var hd = getQueryParameter ( "hd" );
						var loc = getQueryParameter ( "hc" );
						if (name == 'province' && dst != ''){ 
											url = url.replace( "&district="+dst, "");
											if (hd != '')  url = url.replace( "&hd="+hd, "");
											if (loc != '') url = url.replace( "&hc="+loc, "");
											}
						if (name == 'district' && hd != '') {
											url = url.replace( "&hd="+hd, "");
											if (loc != '') url = url.replace( "&hc="+loc, "");
											}
						if (name == 'hd' && loc != '') url = url.replace( "&hc="+loc, ""); 
						
						return url;
							
						}
				function addInURL(name, value){ //alert(name + ", " + value);
						var param = getQueryParameter ( name );
						var url  = document.URL ;
						if (url.indexOf('?') < 0 ){
							 url = url +  "?";
							if (param == "") url += name + "=" + value; //alert(url);
						}else {
							if (param == "") url += "&"+ name + "=" + value; //alert(url);	
							}
						url = make_location_of_parent(name, url); //alert(url)
						url = url.replace("#", '');//alert(url);
						window.location.href = url;
							
						}
				
				function getTotal(province, district, hospital, location, group, subcat){
							
							var prv = getQueryParameter ( "province" );
							var dst = getQueryParameter ( "district" );
							var hd = getQueryParameter ( "hd" );
							var loc = getQueryParameter ( "hc" );
							var param = getQueryParameter ( "summary" );
							var groupurl = getQueryParameter ( "group" );
							var subcaturl = getQueryParameter ( "subcat" );
							var url  = document.URL ;
							if (url.indexOf('?') < 0 ) url = url +  "?";
							if (param != "") {	
										if (url.indexOf('?summary') > -1 )  url = url.replace("?summary="+param, "?");
										else url = url.replace("&summary="+param, "");
										}
							if (province != '' && prv == '' ) url = url + "&province="+ province;
							if (district != '' && dst == '' ) url = url + "&district="+ district;
							if (hospital != '' && hd == '' ) url = url + "&hd="+ hospital;
							if (location != '' && loc == '' ) url = url + "&hc="+ location;
							if ( group && group != '' && groupurl == '' ) url = url + "&group="+ group;
							if ( subcat && subcat != '' && subcaturl == '' ) url = url + "&subcat="+ subcat;
							url = url.replace("#", '');
							//alert(province + "," + district + "," + hd + "," + location + "," + url) ;
							window.location.href = url; 

						}

	function deroulement(form){

				var path=document.URL;
				start = form.start;
				finish = form.finish;
				prv = form.province; 
				dst = form.district;
				hd = form.hd; 
				loc = form.hc;	

		if (path.indexOf("?") < 0 ){ //alert("here1");
				if(start != '' && start != undefined && start != null)path = path +'?start='+start.value;
				if(finish != '' && finish != undefined && finish != null)path = path +'&finish='+finish.value;
				if(prv.value != '' && prv.value != undefined && prv.value != null)path = path +'&province='+prv.value;
				if(dst.value != '' && dst.value != undefined && dst.value != null)path = path +'&district='+dst.value;
				if(hd.value != '' && hd.value != undefined && hd.value != null)path = path +'&hd='+hd.value;
				if(loc.value != '' && loc.value != undefined && loc.value != null)path = path +'&hc='+loc.value;
				window.location=path;	
			}
		else if (((prv.value != '' && prv.value != undefined && prv.value != null) && path.indexOf("province") < 0) || 
				((dst.value != '' && dst.value != undefined && dst.value != null) && path.indexOf("district") < 0) ||
				((hd.value != '' && hd.value != undefined && hd.value != null) && path.indexOf("hd") < 0) || 
				((loc.value != '' && loc.value != undefined && loc.value != null) && path.indexOf("hc") < 0 ) ){
//alert("here2");
			((start != '' && start != undefined && start != null) && path.indexOf("start") < 0)  ? path = path +'&start='+start.value: path=path.replace(/(start=)[^\&]+/, '$1' + start.value);
			((finish != '' && finish != undefined && finish != null)&& path.indexOf("finish") < 0)  ? path = path +'&finish='+finish.value: path=path.replace(/(finish=)[^\&]+/, '$1' + finish.value);
			((prv.value != '' && prv.value != undefined && prv.value != null)&& path.indexOf("province") < 0)  ? path = path +'&province='+prv.value : "";
			((dst.value != '' && dst.value != undefined && dst.value != null) && path.indexOf("district") < 0) ? path = path +'&district='+dst.value: "";
((hd.value != '' && hd.value != undefined && hd.value != null) && path.indexOf("hd") < 0) ? path = path +'&hd='+hd.value: "";
			((loc.value != '' && loc.value != undefined && loc.value != null) && path.indexOf("hc") < 0 )? path = path +'&hc='+loc.value: "";
			
			window.location=path;
			}

		else {  // alert("here3");
			path.indexOf("start") >= 0 ? path=path.replace(/(start=)[^\&]+/, '$1' + start.value) :path=path+'&start='+start.value;
			path.indexOf("finish") >= 0 ? path=path.replace(/(finish=)[^\&]+/, '$1' + finish.value) : path=path +'&finish='+finish.value;
			(path.indexOf("province") >= 0 &&  (prv.value != '' && prv.value != undefined && prv.value != null)) ? path=path.replace(/(province=)[^\&]+/, '$1' + prv.value): path = removeQueryStringParameter(path, ["province", "district", "hd", "hc"]);
			(path.indexOf("district") >= 0 && (dst.value != '' && dst.value != undefined && dst.value != null))? path=path.replace(/(district=)[^\&]+/, '$1' + dst.value):  path = removeQueryStringParameter(path, ["district", "hd", "hc"]);
			(path.indexOf("hd") >= 0 && (hd.value != '' && hd.value != undefined && hd.value != null))? path=path.replace(/(hd=)[^\&]+/, '$1' + hd.value):  path = removeQueryStringParameter(path, ["hd", "hc"]);
			(path.indexOf("hc") >= 0 && (loc.value != '' && loc.value != undefined && loc.value != null)) ? path=path.replace(/(hc=)[^\&]+/, '$1' + loc.value):  path = removeQueryStringParameter(path, ["hc"]);

			//alert("PATH:" + path);
			window.location=path;
				}

			}

			function removeQueryStringParameter(uri, keys) 
						{
						var vre = uri;
						for (i=0; i<keys.length; i++){
							
							var re = new RegExp("([?&])" + keys[i] + "=([a-z0-9]+)", "i");
						    	//var separator = vre.indexOf('?') !== -1 ? "&" : "?";
						    
							    if (vre.match(re)) { 
									vre = vre.replace(re, ''); //alert("PATH FOR "+ keys[i]+" :"+ vre);
								}
							}
						 if(vre.indexOf("?") < 0 ) vre = vre.replace( uri.slice(0, uri.indexOf("?")) , uri.slice(0, uri.indexOf("?")) + "?" );
						 return vre;
						}

function checkArrivalDate(obj){
		//alert("Value: " + obj.value);
		var dtValue = obj.value.split("/");
		var tmValue	= dtValue[2].split(" ");
		var tm = tmValue[1].split(":");
		strValue = new Date(tmValue[0], dtValue[1]-1, dtValue[0], tm[0], tm[1] ); //alert(strValue);
		var varDate = new Date(Date.parse(strValue)); //dd-mm-YYYY
		var today = new Date();
		//alert("SELECTED "+ varDate);
		//alert("TODAY "+ today);
		if( varDate.valueOf() > today.valueOf() ) {
					alert("Arrival date cannot be in the future.");
					//obj.focus();
					obj.value = "";
					return;
					}
		else{
			return true;			
			};
			
	}

function checkDepartureDate( arrobj, obj){
		//alert("Value: " + obj.value +", ARRIVAL: "+ arrobj.value);
		var arrdtValue = arrobj.value.split("/");
		var arrtmValue	= arrdtValue[2].split(" ");
		var arrtm = arrtmValue[1].split(":");
		var arrstrValue = new Date(arrtmValue[0], arrdtValue[1]-1, arrdtValue[0], arrtm[0], arrtm[1] ); //alert(arrstrValue);
		var dtValue = obj.value.split("/");
		var tmValue	= dtValue[2].split(" ");
		var tm = tmValue[1].split(":");
		var strValue = new Date(tmValue[0], dtValue[1]-1, dtValue[0], tm[0], tm[1] );
		var varDate = new Date(Date.parse(strValue)); //dd-mm-YYYY
		var today = new Date();
		//alert("SELECTED "+ varDate);
		//alert("TODAY "+ today);
		if( varDate.valueOf() > today.valueOf() || varDate.valueOf() <  arrstrValue.valueOf() ) {
					alert("Arrival date cannot be in the future or less than arrival datetime.");
					//obj.focus();
					obj.value = "";
					return;
					}
		else{
			return true;			
			};
			
	}

function enable(obj, attrid, value) {
    if (obj.value== value) document.getElementById(attrid).disabled= false;

}

function disable(obj, attrid, value) { //alert(obj.toString());
     if (obj.value== value) document.getElementById(attrid).disabled= true;
     if (!obj.checked) document.getElementById(attrid).disabled= false;
}




				// END FILTERING
				

(function(){

	$card_container = $('#card-container');

	function bakeRows(rows){
		for (var i in rows) {
			var content = '<div class="item-row item-' + rows[i]['fips'] + '">' +
											'<img width="100px" src="images/' + rows[i]['img'] + '"/>' + 
											'<div class="label" style="background-color:#' + rows[i]['hex_code'] + ';">' +
												'<p class="label color">' + rows[i]['country'] + '</p>' +
											'</div>' +
										'</div>'
  		$card_container.append(content);
  	};
	};

	function initIsotope(){
		$card_container.imagesLoaded( function(){
			$card_container.isotope({ 
				item: '.item-row'
			});
		});
	}

	// function initIsotope(){
	// 	$card_container.imagesLoaded( function(){
	// 		$card_container.isotope({
	// 		  getSortData: {
	// 		    name: '.color', // text from querySelector
	// 		    weight: function( itemElem ) { // function
	// 		      var weight = $( itemElem ).find('.weight').text();
	// 		      return parseFloat( weight.replace( /[\(\)]/g, '') );
	// 		    }
	// 		  }
	// 		});
	// 	});
	// }

	$('.item-filter').click(function(){
		var is_active = $(this).hasClass('active');
		if(is_active == false){
			$('.item-filter.active').removeClass('active');
			$(this).addClass('active');
			var filter_by = $(this).data('filter');
			$card_container.isotope({filter: filter_by});
		}else{
			return false
		}
	});

	$.getJSON( "centroids-colors.json", function( rows ) {
		bakeRows(rows)
		initIsotope()
	});
	
}).call(this);
(function ($) {
	$.fn.multiUpload = function (options) {
		// setup default options 
		var defaults = { 
			mw_placeholder:'insert a title',
			mw_text_addBtn:'add',
			mw_tooltip_addBtn:'add a file',
			mw_text_clearBtn:'clear',
			mw_tooltip_clearBtn:'remove all',
			mw_tooltip_removeFileBtn:'remove this file',
			mw_tooltip_removeGroupBtn:'remove this file group',
			mw_group_title:'FILE GROUP',
			mw_fileNumber:true,
			mw_maxElementAllowed:-1 // -1 = no limit
		};
		var options = $.extend({}, defaults, options);
		return this.each(function () {
			if( !( this.tagName == 'INPUT' && this.type == 'file' ) ) {
				alert( 'Error: not a file input element' );
				return;
			}
			// widget
			$(this).addClass('processed');
			var widget = $(this).wrap("<div class='multiupload_widget'></div>");
			// files list
			var files_list = $('<ul class="mw_list"><li style="height:1px;list-style-type:none;">&nbsp;</li></ul>'); // <li style="height:1px;">&nbsp;</li> is a workaround for td height issue in chrome
			$(this).before(files_list);
			// widget bar
			var mwbar = $(this).wrap("<div class='mw_bar'></div>");
			// file title
			var fileTitle = $('<input class="mw_fileTitle" type="text" placeholder="'+options.mw_placeholder+'"/>');
			fileTitle.insertBefore($(this));
			// new element
			var orig_name = $(this).attr('name');
			var element = addElement(	$(this),
										0,
										files_list,
										0,
										orig_name,
										options.mw_fileNumber,
										options.mw_tooltip_removeFileBtn,
										options.mw_tooltip_removeGroupBtn,
										options.mw_group_title,
										options.mw_maxElementAllowed
										)
							.wrap('<div class="mw_fileBrowserWrapper"><a href="javascript:void(0);" class="mw_addBtn" title="'+options.mw_tooltip_addBtn+'"><span>'+options.mw_text_addBtn+'</span></a></div>');
			// clear button
			var clearBtn = $('<a href="javascript:void(0);" class="mw_clearBtn" title="'+options.mw_tooltip_clearBtn+'"><span>'+options.mw_text_clearBtn+'</span></a>');
			clearBtn.click(function(){
				files_list.html('<li style="height:1px;list-style-type:none;">&nbsp;</li>'); // <li style="height:1px;">&nbsp;</li> is a workaround for td height issue in chrome
				$('.mw_fileBrowserWrapper').find('*[input_file_deletable]').each(function(index){
					$(this).remove();
					$('.mw_fileBrowserWrapper').find('input:disabled').removeAttr('disabled');
					$('.mw_addBtn').css({'opacity':'1.0'});
				});
			});
			clearBtn.insertAfter($('.mw_fileBrowserWrapper'));
		});
	};
	function addElement(e,x,f,id,iname,mw_fileNumber,mw_tooltip_removeFileBtn,mw_tooltip_removeGroupBtn,mw_group_title,max) {
		var n = $('.mw_fileBrowserWrapper').find('*[input_file_deletable]').length;
		$(e).css({'position':'absolute','left':'-1500px'});
		$(e).attr('input_file_deletable','');
		var new_element = $('<input name="'+iname+"_"+id+'" type="file" multiple="multiple">');
		var current_element = new_element
		new_element.css({
			'z-index':'100',
			'opacity':'0.0',
			'cursor':'pointer',
			'position':'absolute',
			'left':'-200px'
		})
		if( max != -1 && n >= max-1 ){
			$('.mw_addBtn').css({'opacity':'0.3'});
			new_element.attr("disabled","");
		}
		new_element.change(function(){
			var inp_fileTitle = $('.mw_fileTitle');
			// ms IE9 doesn't support "multiple" attribute in input file
			if ($.browser.msie){
				var multi = false;
			}else{
				var multi = this.files.length==1 ? false : true
			}
			if(multi==false){
				var j=1
				var new_element_prefix = mw_fileNumber===true ? 'File ' + (x + 1) + ': ' : ""
				if (inp_fileTitle.val() != '') {
					var file_item = $('<li title="'+this.value.split(/\\/).pop()+'">'+new_element_prefix+'<i><b><em class=mw_file-ext-'+this.value.split('.').pop().toLowerCase()+'></em></b></i><span>' +inp_fileTitle.val()+'</span></li>');
				} else {
					var file_item = $('<li>'+new_element_prefix+'<i><b><em class=mw_file-ext-'+this.value.split('.').pop().toLowerCase()+'></em></b></i><span>'+this.value.split(/\\/).pop()+'</span></li>');
				}
				var del_item_btn = $('<a class="mw_delItem" href="javascript:void(0);" title="'+mw_tooltip_removeFileBtn+'">x</a>');
				del_item_btn.click(function(){
												$(new_element).remove();
												file_item.remove();
												$(this).remove();
												$('.mw_fileBrowserWrapper').find('input:disabled').removeAttr('disabled');
												$('.mw_addBtn').css({'opacity':'1.0'});
											});
				file_item.prepend(del_item_btn);
				f.append(file_item);
			}else{
				if (inp_fileTitle.val() != '') {
					var files_item = $('<li class="mw_group"><span>'+inp_fileTitle.val()+'</span></li>');
				} else {
					var files_item =$('<li class="mw_group"><span>'+mw_group_title+'</span></li>');
				}
				files_item.click(function(){
					$(this).children('ul').slideToggle('slow');
				});
				var group = $('<ul> </ul>');
				for (var j = 0; j < this.files.length; j++) {
					var new_element_prefix = mw_fileNumber===true ? 'File ' + (j + x + 1) + ': ' : ""
					var file_item = $('<li>'+new_element_prefix+'<i><b><em class=mw_file-ext-'+this.files[j].name.split('.').pop().toLowerCase()+'></em></b></i><span>'+this.files[j].name+'</span></li>');
					group.append(file_item);
				}
				files_item.append(group);
				var del_item_btn = $('<a class="mw_delItem" href="javascript:void(0);" title="'+mw_tooltip_removeGroupBtn+'">x</a>');
				del_item_btn.click(function(){
												$(new_element).remove();
												files_item.remove();
												$(this).remove();
												$('.mw_fileBrowserWrapper').find('input:disabled').removeAttr('disabled');
												$('.mw_addBtn').css({'opacity':'1.0'});
											});
				files_item.prepend(del_item_btn);
				f.append(files_item);
			}
			origName = new_element.attr('name');
			new_element.attr('name', origName+":"+inp_fileTitle.val()); // TODO: could this be made better? 
																		// I mean, the title must be appended to element's name 
																		// or is there another way?
			inp_fileTitle.val('');
			addElement($(new_element),j+x,f,id+1,iname,mw_fileNumber,mw_tooltip_removeFileBtn,mw_tooltip_removeGroupBtn,mw_group_title,max);
		})
		e.before(new_element);
		return new_element;
	}
})(jQuery);
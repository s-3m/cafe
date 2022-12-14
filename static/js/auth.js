
$(function(){
	window.tobiz_auth = (function () {
		var app = {
			initState: 0,
			authState: 0,
			user: '',
			debug:0,
			alert: function(type, text){
				var id = 'alert_id_' + app.uuid();
				 $('body .alerts > .alert').remove();


				$('body .alerts').append('<div id="'+id+'" class="type_'+type+' alert">'+text+'</div>');
				setTimeout(function(){
					$('#'+id).remove();
				},2500);

			},
			uuid: function() {
				return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
				  (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
				);
			},
			log: function(mixed) {

				if(app.debug==1){
					console.log(mixed);
				}

			},
			ajaxSuccess : function(data){
				app.log(data);
				if(data.status=='Error'){
					switch (data.request.action){
						case 'checkSession':
							app.logout();
							break;
						case 'registration':
						case 'login' :
							app.alert('error', data.description);
							break;
						case 'forgotPassword' :
							app.alert('error', data.description);
					}
				}
				if(data.status=='Success'){
					switch (data.request.action){
						case 'login' :
						case 'registration':

//                            console.log([data.cookie.email,data.cookie.session]);
//
//                            app.cookie.set('email',data.cookie.email,14 );
//                            app.cookie.set('session',data.cookie.session,14);
//
//                            console.log();





							app.destroyAuthForm();
							app.checkSession();
							break;
						case 'checkSession':
							app.user = data.user.email;
							app.login();
							break;

						case 'forgotPassword':
							app.alert('success', data.description);
							app.destroyForgotPassword();
							break;
					}
				}
			},

			ajaxError : function(data){
				app.log('ajax error');
				app.log(data);
			},

			ajaxSend: function (options) { // nice wrap
				var success = options.success  || app.ajaxSuccess || function () {};
				var error = options.onerror || app.ajaxError || function () {};
				var data = options.data || {};
				$.ajax({
					url: '/auth.php',
					type: 'POST',
					dataType:'json',
					data: data,
					async: false,
					cache: false,
					contentType: false,
					processData: false,
					xhrFields: {
						withCredentials: true
					},                    
					success: success,
					error: error
				});

			},
			url:  {
				getParam: function (name, url) {
					if (!url) url = window.location.href;
						name = name.replace(/[\[\]]/g, '\\$&');
					var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
						results = regex.exec(url);
					if (!results) return null;
					if (!results[2]) return '';
					return decodeURIComponent(results[2].replace(/\+/g, ' '));
				}
			},
			cookie: {
					set: function(name,value,days) {
						var expires = "";
						if (days) {
							var date = new Date();
							date.setTime(date.getTime() + (days*242424*60*60*1000));
							expires = "; expires=" + date.toUTCString();
						}
						document.cookie = name + "=" + (value || "")  + expires + "; path=/";
					},
					get: function (name) {
						var nameEQ = name + "=";
						var ca = document.cookie.split(';');
						for(var i=0;i < ca.length;i++) {
							var c = ca[i];
							while (c.charAt(0)==' ') c = c.substring(1,c.length);
							if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
						}
						return null;
					},
					remove: function (name) {
						document.cookie = name+'=; Max-Age=-99999999;';
					}

			},

			destroyAuthForm:function(){
				$('.auth_form').remove();
			},
			destroyOrders:function(){
				$('.my_orders').remove();
			},
			destroyPP:function(){
				$('.my_pp').remove();
			},
			destroyForgotPassword:function(){
				$('.forgot_password').remove();
			},

			renderOrders: function(page=1){
				app.destroyOrders();

				var orders = '?????? ??????????????.';
				var class_name = '';
				var paginator = '';
				var total_orders = 0;
				var formData = new FormData();
					formData.append('action', 'getOrders');
					formData.append('page', page);

				app.ajaxSend({
					data: formData,
					success: function(data){
						app.log(data);
						app.log(data.orders);


						if(data.status=='Success'){

							orders='';
							$.each(data.orders, function(idx,order){

								orders+=`<div class="order">
										<div class="order_row">
											<div class="id"><span>??? ${order.id}</span> <span>???? ${order.created} </span></div>
											<div class="user_status">${order.customer_status ? order.customer_status : '' }</div>
											<div class="user_email">${order.user_email}</div>
											<div class="user_phone">${order.user_phone}</div>
											<div class="user_name">${order.uname}</div>
											<div class="more">??????????????????</div>
										</div>

										<div class="info">${order.user_name} <div>${order.admin_comment}</div></div>

									</div>`;

							})

							paginator = '';
							var pages = Math.ceil(data.total/10);

							for(i=1; i<=pages; i++){
								class_name = '';
								if(page==i){
									class_name = 'current';

								}
								paginator += '<span data-page="'+i+'" class=" page_picker '+class_name+'">'+i+'</span>';


							}
							total_orders = data.total;

							app.log(orders);
						}


					}
				});

				var myOrders = `<div class="my_orders">
					<div class="my_orders_wrapper">
						<div class="my_orders_close">??</div>

						<div class="my_orders_title">???????????? ??????????????: ${total_orders}</div>

						<div class="my_orders_list">${orders}</div>

						<div class="my_orders_paginator">${paginator}</div>

					</div>
				</div>`;



				$('body').append(myOrders);






			},
			renderPP: function(page=1){
				app.destroyPP();

				var response ;
				var stat = '?????? ????????????.';
				var class_name = '';
				var formData = new FormData();
					formData.append('action', 'getPPstat');

				app.ajaxSend({
					data: formData,
					success: function(response){
						console.log(response);
						if(response.status=='Success'){
							var myStat = `<div class="my_pp">
								<div class="my_pp_wrapper">
									<div class="my_pp_close">??</div>
									<div class="my_pp_title">?????????????????????? ??????????????????</div>

									<div class="rr">?????? E-mail: ${response.data.email}</div>
									<div class="rr">?????????????????????? ????????????: <a target="_blank" href="${response.data.link}">${response.data.link}</a> </div>
									<div class="rr pt30">?????????????? ?????????????????????? ??????????????????: ${response.data.terms}</div>
									<div class="rr">??????????????????: <b>${response.data.bonusPlus}</b></div>
									<div class="rr">??????????????????: <b>${response.data.bonusMinus}</b></div>
									<div class="rr">??????????: <b>${response.data.bonusTotal}</b></div>

									<div class="my_pp_title">???????????????????? ?????????????????????? ??????????????????</div>
									<div>

										<div class="row">
											<div class="col"></div>
											<div class="col">????????????</div>
											<div class="col">??????????</div>
											<div class="col">?????? ??????????</div>
										</div>
										<div class="row">
											<div class="col">??????????</div>
											<div class="col">${response.data.clicks.week}</div>
											<div class="col">${response.data.clicks.month}</div>
											<div class="col">${response.data.clicks.all}</div>
										</div>
										<div class="row">
											<div class="col">????????????</div>
											<div class="col">${response.data.orders.week}</div>
											<div class="col">${response.data.orders.month}</div>
											<div class="col">${response.data.orders.all}</div>
										</div>


									</div>
									<div class="rr pt30">?????? ?????????????????? ?????????????????????? ???????????? ???????????????? ???? : ${response.data.owner}</div>
								</div>
							</div>`;
							$('body').append(myStat);
						}
					}
				});

			},
			renderForgotPassword: function(){
				app.destroyAuthForm();
				app.destroyForgotPassword();

				var forgotPassword = `
				<div class="forgot_password">
					<div class="forgot_password_wrapper">
						<div class="forgot_password_close">??</div>
						<div class="row">
							<div class="col">
							   <div class="forgot_password_title">???????????? ????????????</div>
								<form method="POST">
									<input type="hidden" value="forgotPassword" name="action" />
									<div class="field">
										<lable>?????????????? E-Mail</lable>
										<input type="email" value="" placeholder="E-mail" name="email" required="required" />
									</div>

									<div class="field">
										<button>???????????????????????? ????????????</button>
									</div>


								</form>
							</div>

						</div>
					</div>
				</div>

				`;



				$('body').append(forgotPassword);

			},
			renderAuthForm: function(){
				app.destroyAuthForm();
				var authForm = `
				<div class="auth_form">
					<div class="auth_form_wrapper">
						<div class="auth_form_close">??</div>
						<div class="row">
							<div class="col">
							   <div class="auth_form_title">??????????????????????</div>
								<form method="POST">
									<input type="hidden" value="registration" name="action" />
									<div class="field">
										<lable>?????????????? ??????</lable>
										<input type="text" value="" placeholder="??????" name="name" />
									</div>
									<div class="field">
										<lable>?????????????? E-Mail</lable>
										<input type="email" value="" placeholder="E-mail" name="email" required="required" />
									</div>
									<div class="field">
										<lable>?????????????? ??????????????</lable>
										<input type="text" value="" placeholder="??????????????" name="phone" />
									</div>
									<div class="field">
										<lable>?????????????? ????????????</lable>
										<input type="text" value="" placeholder="????????????" name="password" />

									</div>
									<div class="field">
										<button>????????????????????????????????</button>
									</div>


								</form>
							</div>
							<div class="col">

							   <div class="auth_form_title">????????</div>
								<form method="POST">
									<input type="hidden" value="login" name="action" />
									<div class="field">
										<lable>?????????????? E-Mail</lable>
										<input type="email" value="" placeholder="email" name="email" required="required" />
									</div>

									<div class="field">
										<lable>?????????????? ????????????</lable>
										<input type="password" value="" placeholder="password" name="password" required="required" />
									</div>
									<div class="field">
										<button>??????????</button> <span class="forgot_password_show_form">???????????? ????????????</span>
									</div>


								</form>

							</div>

						</div>
					</div>
				</div>

				`;



				$('body').append(authForm);

			},


			checkSession: function(){
				var formData = new FormData();
				formData.append('action', 'checkSession');
				app.ajaxSend({data: formData});
			},

			passwordRecovery: function(){},
			myOrders: function(){},

			logout: function(){
				app.log('logout')
				app.authState=0;
				$('.tobiz_auth').html('<div class="auth"><span class="svg-icon-padlock-with-a-heart"></span> <span> ???????? / ??????????????????????</span></div>');


			},
			login: function(){
				app.log('login')
				app.authState=1;


				let pp = '';

				if(window.tobiz.pp*1 == 1){
					pp = '<div class="my_pp_show"><span class="svg svg-icon-ocument"></span>&nbsp;&nbsp;?????????????????????? ??????????????????</div>';
				}




				$('.tobiz_auth').html('<div class="user"><span class="svg-icon-padlock-with-a-heart"></span> '+app.user+'<div class="popup_user"><div class="my_orders_show"><span class="svg svg-icon-ocument"></span>&nbsp;&nbsp;???????????? ??????????????</div> '+pp+' <div class="logout"><span class="svg-icon-padlock-with-a-heart"></span>&nbsp;&nbsp;??????????</div></div> ');
				app.destroyAuthForm();

			},


			eventListener: function(){

				$('body').on('click', '.tobiz_auth .my_orders_show', function (){
					app.log('?????????????? ???????? c ????????????????.');
					app.renderOrders();
				});
				$('body').on('click', '.tobiz_auth .my_pp_show', function (){
					app.log('?????????????? ???????? c?? ?????????????????????? ?????????????????????? ??????????????????.');
					app.renderPP();
				});
				$('body').on('click', '.tobiz_auth .logout', function (){
					app.log('??????????.');
					var formData = new FormData();
					formData.append('action', 'logout');
					app.ajaxSend({data: formData, success:function(){

						app.logout();
						app.alert('success', '???????????? ??????????????????.');

					}});


				});

				$('body').on('click' ,'.forgot_password_close', function(){
					app.log('?????????????? ???????? ?? ????????????????.');
					app.destroyForgotPassword();
				});
				$('body').on('click' ,'.my_orders_close', function(){
					app.log('?????????????? ???????? ?? ????????????????.');
					app.destroyOrders();
				});

				$('body').on('click', '.tobiz_auth .auth', function (){
					app.log('?????????????? ???????? ?????????????????????? / ??????????????????????.');
					app.renderAuthForm();
				});
				$('body').on('click', '.forgot_password_show_form', function (){
					app.log('?????????????? ???????? ???????????? ????????????.');
					app.renderForgotPassword();
				});

				$('body').on('click', '.my_orders .order .more', function (){
					app.log('???????????????? ???????????? ???????????????? ????????????.');
					$('.my_orders .order .info').hide();
					$(this).parent().parent().children('.info').toggle();
				});
				$('body').on('click', '.my_orders .page_picker', function (){
					app.log('???????????????? ???????????? ????????????????.');
					app.renderOrders($(this).data('page'));
					$(this).parent().parent().children('.info').toggle();
				});


				$('body').on('submit', '.auth_form form ', function (event){
					app.log('???????????????? ??????????');
					event.stopPropagation();
					event.preventDefault();
					app.ajaxSend({data: new FormData($(this)[0])});
				});


				$('body').on('submit', '.forgot_password form ', function (event){
					app.log('???????????????? ?????????? ???????????????????????????? ????????????');
					event.stopPropagation();
					event.preventDefault();
					app.ajaxSend({data: new FormData($(this)[0])});
				});

				$('body').on('click' ,'.auth_form_close', function(){
					app.log('?????????????? ???????? ?????????????????????? / ??????????????????????.');
					app.destroyAuthForm();
				});
				$('body').on('click' ,'.my_pp_close', function(){
					app.destroyPP();
				});

			},
			init: function(){





				if(!app.initState==0){
					return;
				}
//                $('#wrapper').prepend('<div class="block tobiz_auth"></div>');
				app.checkSession();
				app.eventListener();



				$('body').prepend('<div class="alerts"></div>');

				var get_tobiz_auth = app.url.getParam('tobiz_auth');
				var get_tobiz_auth_msg = app.url.getParam('msg');
				if(get_tobiz_auth && get_tobiz_auth_msg){
					app.alert(get_tobiz_auth, get_tobiz_auth_msg);
				}

			}

		}





		//
		app.init();
		return app;

	})()

})
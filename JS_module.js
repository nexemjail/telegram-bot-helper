var watson = require('watson-developer-cloud');
var myLib = require('./JS_lib');
var Q = require('q');

var personalityInsights = watson.personality_insights({
	username: '0d049ae6-affa-4f05-8b96-170001be0c39',
	password: 'KamNU6jAjxEH',
	url: "https://gateway.watsonplatform.net/personality-insights/api",
	version: 'v2'
});

function get_PI_from_text(text){
	var result;
	personalityInsights.profile({
		  text: text,
		  language: 'en' },
		  function (err, resp) {
			if (err)
			  console.log('error:', err);
			else{
				result = myLib.PI_to_array(resp);
			};
		})
	);
};

function work_with_promise(account){
	var deferred = Q.defer();
		console.log('go go go');
		setTimeout(function () {
			deferred.resolve('OOOOOOOUUUUUUEEEEEE');
			
		}, 10000);
		console.log('NOOOOOOOOOOOOOOOO');
		return deferred.promise;
};

function get_PI_from_twitter(account){
	var result;
	var text = myLib.get_tweets_as_text(account);
	result = get_PI_from_text(text);
	return result;
};
var watson = require(process.cwd() + '/node_modules/watson-developer-cloud');
var myLib = require(process.cwd() + '/JS_lib');

var personalityInsights = watson.personality_insights({
	username: '601a832f-ba02-48ca-9b9d-cfa459855ee0',
	password: 'ud7qdp2c0xK4',
	url: "https://gateway.watsonplatform.net/personality-insights/api",
	version: 'v2'
});

function get_PI_from_text(text){
	var result;
	personalityInsights.profile({
		  text: text,
		  language: 'en' },
		  function (err, resp) {
			if (err) {
                console.log('error:', err);
            }
			else{
				result = myLib.PI_to_array(resp);
			};
		}
	);
    return result;
};



function get_PI_from_twitter(account){
	var result;
	var text = myLib.get_tweets_as_text(account);
	result = get_PI_from_text(text);
	return result;
};

exports.get_PI_from_text = get_PI_from_text;
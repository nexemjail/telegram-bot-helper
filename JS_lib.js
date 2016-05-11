var twitterAPI = require('node-twitter-api');
var twitter = new twitterAPI({
	consumerKey: '9kwjYTUFNjsZOYorBine12DTg',
	consumerSecret: '5GRIwi1laTHBCc2WAvflavE0scvDeGCC4cscjOZq1WPAbBHkBd',
	callback: ''
});

var token, secretToken;

function PI_to_array(PI){
	var result = [];
	var big5 = PI.tree.children[0],
		needs = PI.tree.children[1],
		values = PI.tree.children[2];
		
	big5.children.forEach(function(item){
		result.push(make_array(item, 'Big 5'));
	});
	
	needs.children.forEach(function(item){
		result.push(make_array(item, 'Needs'));
	});
	
	values.children.forEach(function(item){
		result.push(make_array(item, 'Values'));
	});
	return result;
};

function make_array(object, mainParent){
	var result = [];
	var parent = object.id;
	result.push({
		name: object.id,
		parent: mainParent,
		value: object.percentage
	});
	object.children.forEach(function(item){
		result.push({
			name: item.id,
			parent: parent,
			value: item.percentage
		});
	});
	return result;
};

function tweetToContentText(tweets) {
  var result = '';
  tweets.forEach(function(item, i){
	 if (i !=0){
		result = item.text + ' ' + result;
	 };
  });
  return result;
};

function get_tweets_as_text(account){
	var requestToken, requestTokenSecret;
	var text;
	twitter.getRequestToken(function(error, requestToken, requestTokenSecret, results){
		if (error) {
			console.log("Error getting OAuth request token : " + error);
		} else {
			 requestToken = requestToken;
			 requestTokenSecret = requestTokenSecret;
		};
	});
	console.log('got request token '+requestToken);
	twitter.getAccessToken(requestToken, requestTokenSecret, oauth_verifier, function(error, accessToken, accessTokenSecret, results) {
		if (error) {
			console.log(error);
		} else {
			token = accessToken;
			secretToken = accessTokenSecret;
		};
	});
	console.log('got access token '+token);
	twitter.getTimeline("user_timeline", {
							screen_name: account
						},
						token,
						secretToken,
						function(error, data, response){
							if (error){
								console.log(error);
							} else {
								text = tweetToContentText(data);
							};
						});
	console.log('got text '+text);
	return text;
};

exports.PI_to_array = PI_to_array;
exports.get_tweets_as_text = get_tweets_as_text;
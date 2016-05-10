define([
    '../module',
    '../namespace',
], function (module, namespace, app) {
    var name = namespace + '.mainController';

    var dependencies = ['$scope', namespace + '.mainService'];

    var controller = function ($scope, mainService) {
		$scope.Openness = 0;
		$scope.Conscientiousness = 0;
		$scope.Extraversion = 0;
		$scope.Agreeableness = 0;
		$scope.Neuroticism = 0;
		$scope.max = 100;
		
        $scope.showResult = function(){
			var data = {text: $scope.text};
            mainService.getResult(data).then(function (res) {
                var bigFive = res.data.tree.children[0].children[0].children;
				bigFive.forEach(function(item){
					$scope[item.id] = Math.round(item.percentage * 100);
				});
				
            });
        }
    };
    module.controller(name, dependencies.concat(controller));
})
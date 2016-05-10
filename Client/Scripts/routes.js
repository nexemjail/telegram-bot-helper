define(['./namespace', 'angular', './app'], function (namespace, angular) {
    'use strict';
    var app = angular.module(namespace);

    app.run(function ($rootScope) {
        $rootScope.$on('$stateChangeError', function () {
            console.error(arguments[5]);
        });
    });

    app.config(['$stateProvider', '$urlRouterProvider', function ($stateProvider, $urlRouterProvider) {
        $urlRouterProvider.otherwise('/home');
        $stateProvider
        .state('home', {
            url: "/home",
            controller: "PI_Sample.common.mainController",
            templateUrl: "Scripts/common/templates/_mainLayout.html"
        })
    }]);

});
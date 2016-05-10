define([
     'angular',
     './namespace',
     './common/namespace',
     'angularUiRouter',
     'angularLocalStorage',
     'angularUiBootstrap',
     'angularResource',
     'angularLocale',
	 'angularAnimate',
     './common/require',
], function (angular, namespace, common) {
    'use strict';

    var name = namespace;

    return angular.module(name, [common, 'ui.router', 'LocalStorageModule', 'ngResource', 'ui.bootstrap', 'ngAnimate' ]);
});
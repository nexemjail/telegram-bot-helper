define([
    '../namespace',
    '../module'
],
function (namespace, module) {
    'use strict';

    var factoryId = 'mainService';
    var name = namespace + "." + factoryId;
    var dependencies = ['$http'];
    var service = function ($http) {
        var serviceBaseUri = '/sample';
        var mainServiceFactory = {};

        var _getResult = function (data) {
            var serviceUri = serviceBaseUri;
            var config = {
                headers: {
                    'Accept': 'application/json'
                }
            };
            return $http.post(serviceUri, data, config);
        };

        mainServiceFactory.getResult = _getResult;

        return mainServiceFactory;
    };

    module.factory(name, dependencies.concat(service));
})
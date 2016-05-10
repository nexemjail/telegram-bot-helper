define([
    './namespace',
    'angular'
], function (namespace, angular) {
    'use strict';

    var name = namespace;

    var module = angular.module(name, []);

    return module;
})
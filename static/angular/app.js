/**
 * Created by markdaniel on 10/17/15.
 */
var crime_cast_app = angular.module('crime_cast_app', ['ui.router', 'ngRoute']);

crime_cast_app.config(['$stateProvider', '$urlRouterProvider',
    function($stateProvider, $urlRouterProvider) {
        $stateProvider.state('splash', {
            url: '/splash',
            templateUrl: 'splash.html',
            controller: 'crime_cast_ctrl'
        }).state('crimes', {
            url: '/crimes',
            templateUrl: 'crimes.html',
            controller: 'crime_cast_ctrl'
        }).state('weeks', {
            url: '/weeks',
            templateUrl: 'weeks.html',
            controller: 'crime_cast_ctrl'
        }).state('crime_types', {
            url: '/crime_types',
            templateUrl: 'crime_types.html',
            controller: 'crime_cast_ctrl'
        }).state('zips', {
            url: '/zips',
            templateUrl: 'zips.html',
            controller: 'crime_cast_ctrl'
        }).state('about', {
            url: '/about',
            templateUrl: 'about.html',
            controller: 'crime_cast_ctrl'
        })
        $urlRouterProvider.otherwise('splash');
    }]);
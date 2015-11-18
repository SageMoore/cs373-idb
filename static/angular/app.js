/**
 * Created by markdaniel on 10/17/15.
 */
var crimeCastApp = angular.module('crimeCastApp', ['ui.router', 'ngRoute', 'crimeCastApp.httpServices', 'crimeCastApp.services', 'ngTable']);

crimeCastApp.config(['$stateProvider', '$urlRouterProvider', '$locationProvider',
    function($stateProvider, $urlRouterProvider, $locationProvider) {

        $locationProvider.html5Mode(true);

        $stateProvider.state('splash', {
            url: '/splash',
            templateUrl: 'splash.html',
            controller: 'crimeCastCtrl'
        }).state('results', {
            url: '/results/:query',
            templateUrl: 'results.html',
            controller: 'resultsCtrl'
        }).state('about', {
            url: '/about',
            templateUrl: 'about.html',
            controller: 'aboutCtrl'
        }).state('crimes', {
            url: '/crimes',
            templateUrl: 'crimes.html',
            controller: 'crimesCtrl'
        }).state('crimes/:crimeId', {
            url: '/crimes/:crimeId',
            templateUrl: 'crime.html',
            controller: 'crimeCtrl'
        }).state('crime_types', {
            url: '/crime_types',
            templateUrl: 'crimetypes.html',
            controller: 'crimeTypesCtrl'
        }).state('crime_types/:crime_type_id', {
            url: '/crime_types/:crime_type_id',
            templateUrl: 'crime_type.html',
            controller: 'crimeTypeCtrl'
        }).state('weeks', {
            url: '/weeks',
            templateUrl: 'weeks.html',
            controller: 'weeksCtrl'
        }).state('weeks/:week_id', {
            url: '/weeks/:week_id',
            templateUrl: 'week.html',
            controller: 'weekCtrl'
        }).state('zips', {
            url: '/zips',
            templateUrl: 'zips.html',
            controller: 'zipsCtrl'
        }).state('zips/:zip_id', {
            url: '/zips/:zip_id',
            templateUrl: 'zip.html',
            controller: 'zipCtrl'
        });
        $urlRouterProvider.otherwise('splash');

    }]);

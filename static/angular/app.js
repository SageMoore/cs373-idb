/**
 * Created by markdaniel on 10/17/15.
 */
var crimeCastApp = angular.module('crimeCastApp', ['ui.router', 'ngRoute', 'crimeCastApp.httpServices', 'crimeCastApp.services']);

crimeCastApp.config(['$stateProvider', '$urlRouterProvider', '$locationProvider',
    function($stateProvider, $urlRouterProvider, $locationProvider) {

        $locationProvider.html5Mode(true);

        $stateProvider.state('splash', {
            url: '/splash',
            templateUrl: 'splash.html',
            controller: 'crimeCastCtrl'
        }).state('about', {
            url: '/about',
            templateUrl: 'about.html',
            controller: 'crimeCastCtrl'
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
        }).state('crime_types/:crime_type', {
            url: '/crime_types/:crime_type_id',
            templateUrl: 'crimetype.html',
            controller: 'crimeTypeCtrl'
        }).state('weeks', {
            url: '/weeks',
            templateUrl: 'weeks.html',
            controller: 'weeksCtrl'
        }).state('weeks/:week', {
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

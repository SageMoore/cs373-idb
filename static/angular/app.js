/**
 * Created by markdaniel on 10/17/15.
 */
var crimeCastApp = angular.module('crimeCastApp', ['ui.router', 'ngRoute']);

crimeCastApp.config(['$stateProvider', '$urlRouterProvider', '$routeProvider', '$locationProvider',
    function($stateProvider, $urlRouterProvider, $routeProvider, $locationProvider) {

        $locationProvider.html5Mode(true);

        $stateProvider.state('splash', {
            url: '/splash',
            templateUrl: 'splash.html',
            controller: 'crimeCastCtrl'
        }).state('crimes', {
            url: '/crimes',
            templateUrl: 'crimes.html',
            controller: 'crimeCastCtrl'
        }).state('weeks', {
            url: '/weeks',
            templateUrl: 'weeks.html',
            controller: 'crimeCastCtrl'
        }).state('week1', {
            url: '/week1',
            templateUrl: 'week1.html',
            controller: 'crimeCastCtrl'
        }).state('week2', {
            url: '/week2',
            templateUrl: 'week2.html',
            controller: 'crimeCastCtrl'
        }).state('week3', {
            url: '/week3',
            templateUrl: 'week3.html',
            controller: 'crimeCastCtrl'
        }).state('crime_types', {
            url: '/crime_types',
            templateUrl: 'crimetypes.html',
            controller: 'crimeCastCtrl'
        }).state('zips', {
            url: '/zips',
            templateUrl: 'zips.html',
            controller: 'crimeCastCtrl'
        }).state('zips1', {
            url: '/zips1',
            templateUrl: 'zips1.html',
            controller: 'crimeCastCtrl'
        }).state('zips2', {
            url: '/zips2',
            templateUrl: 'zips2.html',
            controller: 'crimeCastCtrl'
        }).state('zips3', {
            url: '/zips3',
            templateUrl: 'zips3.html',
            controller: 'crimeCastCtrl'
        }).state('about', {
            url: '/about',
            templateUrl: 'about.html',
            controller: 'crimeCastCtrl'
        }).state('crime1', {
            url: '/crime1',
            templateUrl: 'crime1.html',
            controller: 'crimeCastCtrl'
        }).state('crime2', {
            url: '/crime2',
            templateUrl: 'crime2.html',
            controller: 'crimeCastCtrl'
        }).state('crime3', {
            url: '/crime3',
            templateUrl: 'crime3.html',
            controller: 'crimeCastCtrl'
        }).state('crimetype1', {
            url: '/crimetype1',
            templateUrl: 'crimetype1.html',
            controller: 'crimeCastCtrl'
        }).state('crimetype2', {
            url: '/crimetype2',
            templateUrl: 'crimetype2.html',
            controller: 'crimeCastCtrl'
        }).state('crimetype3', {
            url: '/crimetype3',
            templateUrl: 'crimetype3.html',
            controller: 'crimeCastCtrl'
        });
        $urlRouterProvider.otherwise('splash');

    }]);

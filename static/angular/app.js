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
        }).state('week1', {
            url: '/week1',
            templateUrl: 'week1.html',
            controller: 'crime_cast_ctrl'
        }).state('week2', {
            url: '/week2',
            templateUrl: 'week2.html',
            controller: 'crime_cast_ctrl'
        }).state('week3', {
            url: '/week3',
            templateUrl: 'week3.html',
            controller: 'crime_cast_ctrl'
        }).state('crime_types', {
            url: '/crime_types',
            templateUrl: 'crimetypes.html',
            controller: 'crime_cast_ctrl'
        }).state('zips', {
            url: '/zips',
            templateUrl: 'zips.html',
            controller: 'crime_cast_ctrl'
        }).state('zips1', {
            url: '/zips1',
            templateUrl: 'zips1.html',
            controller: 'crime_cast_ctrl'
        }).state('zips2', {
            url: '/zips2',
            templateUrl: 'zips2.html',
            controller: 'crime_cast_ctrl'
        }).state('zips3', {
            url: '/zips3',
            templateUrl: 'zips3.html',
            controller: 'crime_cast_ctrl'
        }).state('about', {
            url: '/about',
            templateUrl: 'about.html',
            controller: 'crime_cast_ctrl'
        }).state('crime1', {
            url: '/crime1',
            templateUrl: 'crime1.html',
            controller: 'crime_cast_ctrl'
        }).state('crime2', {
            url: '/crime2',
            templateUrl: 'crime2.html',
            controller: 'crime_cast_ctrl'
        }).state('crime3', {
            url: '/crime3',
            templateUrl: 'crime3.html',
            controller: 'crime_cast_ctrl'
        }).state('crimetype1', {
            url: '/crimetype1',
            templateUrl: 'crimetype1.html',
            controller: 'crime_cast_ctrl'
        }).state('crimetype2', {
            url: '/crimetype2',
            templateUrl: 'crimetype2.html',
            controller: 'crime_cast_ctrl'
        }).state('crimetype3', {
            url: '/crimetype3',
            templateUrl: 'crimetype3.html',
            controller: 'crime_cast_ctrl'
        });
        $urlRouterProvider.otherwise('splash');
    }]);

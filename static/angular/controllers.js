'use strict';
crimeCastApp.controller('crimeCastCtrl', function($scope, services, http_service) {

    services.getMap();

    $scope.sortType     = 'id'; // set the default sort type
    $scope.sortReverse  = false;  // set the default sort order

}).controller('crimesCtrl', function ($scope, http_service, services, disqusApi, $location) {

    var map = services.getMap();

    var params = {
        limit: 5,
        related: 'thread'
    }

    disqusApi.get('forums', 'listPosts', params).then(function (comments) {
        $scope.comments = comments;
        console.log(comments);
    });

    var loadAllWidgets = function() {
        !function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+"://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");
    };

    var destroyAllWidgets = function() {
        var $ = function (id) { return document.getElementById(id); };
        var twitter = $('twitter-wjs');
        if (twitter != null)
            twitter.remove();
    };

    destroyAllWidgets();
    loadAllWidgets();


    var getCrimes = function() {
        http_service.getRequestGeneric('crimes').then(function(data) {
            console.log('data for crimes is...: ', data);
            $scope.crimes = data;
            angular.forEach($scope.crimes, function(value, key) {
                services.addMarker(value.lat, value.lng, value.address, map, value.crime_type.crime_type_name);
            })
        })
    }

    $scope.crimes = getCrimes();

}).controller('crimeCtrl', function ($scope, http_service, $location, $stateParams) {

    var crimeId = $stateParams.crimeId;

    var getCrime = function(crimeId) {
        http_service.getCrime(crimeId).then(function(data) {
            $scope.crime = data;
        })
    }

    $scope.crime = getCrime(crimeId);

}).controller('crimeTypesCtrl', function ($scope, http_service, services, $location) {

    var getCrimeTypes = function() {
        http_service.getRequestGeneric('crime_types').then(function(data) {
            $scope.crimeTypes = data;
            console.log('data for crimetypes is...: ', data);
        })
    };

    var goToCrimeType = function (crimeId) {
        $location.path('/crime_types/' + crimeId);
    };

    $scope.crimeTypes = getCrimeTypes();
    $scope.goToCrimeType = goToCrimeType;

}).controller('crimeTypeCtrl', function ($scope, http_service, $location, $stateParams) {

    var crimeId = $stateParams.crimeTypeId;

    var getCrimeType = function(crimeTypeId) {
        http_service.getCrimeType(crimeTypeId).then(function(data) {
            $scope.crimeType = data;
        })
    };

    $scope.crimeType = getCrimeType(crimeId);

}).controller('weeksCtrl', function ($scope, http_service, services, $location) {

    var getWeeks = function() {
        http_service.getRequestGeneric('weeks').then(function(data) {
            $scope.weeks = data;
            console.log('data for weeks is...: ', data);
        })
    };

    var goToWeek = function (weekId) {
        $location.path('/weeks/' + weekId);
    };

    $scope.weeks = getWeeks();
    $scope.goToWeek = goToWeek;

}).controller('weekCtrl', function ($scope, http_service, $location, $stateParams) {

    var weekId = $stateParams.weekId;

    var getWeek = function(weekId) {
        http_service.getWeek(weekId).then(function(data) {
            $scope.week = data;
        })
    };

    $scope.week = getWeek(weekId);

}).controller('zipsCtrl', function ($scope, http_service, services, $location) {

    var getZips = function() {
        http_service.getRequestGeneric('zips').then(function(data) {
            $scope.zips = data;
            console.log('data for zips is...: ', data);
        })
    };

    var goToZip = function (zipId) {
        $location.path('/zips/' + zipId);
    };

    getZips();
    $scope.goToZip = goToZip;

}).controller('zipCtrl', function ($scope, http_service, $location, $stateParams) {

    var zipId = $stateParams.zipId;

    var getZip = function(zipId) {
        http_service.getZip(zipId).then(function(data) {
            $scope.zip = data;
        })
    };

    $scope.zip = getZip(zipId);

}).controller('aboutCtrl', function ($scope, http_service, $location, $stateParams) {
    $scope.results = "No test results yet..."

    $scope.runTests = function() {
        http_service.getRequestGeneric('tests').then(function(data) {
            $scope.results = data.results;
        })
    };
});
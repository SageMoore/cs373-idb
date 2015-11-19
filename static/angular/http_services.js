'use strict';

angular.module('crimeCastApp.httpServices', [])
    .factory('http_service', function($http, $q){
        return {
            getRequestGeneric : getRequestGeneric,
            postRequestGeneric : postRequestGeneric,
            getCrime : getCrime,
            getCrimeType : getCrimeType,
            getWeek : getWeek,
            getZip : getZip,
            getCars: getCars
        }

        function getRequestGeneric(pathParam){
            return $http
                .get(
                '/api/v1/' + pathParam ).then(function(response) {
                    return JSON.parse(response.data);
                }, function(response){
                    console.log('rejecting promise');
                    return $q.reject(response.data);
                });
        }

        function getCars() {
            //return $http.get('http://162.242.248.195/model_api').then(function(response) {
            return $http.get('/../cars.json').then(function(response) {
                    console.log('data is: ', response.data);
                    return JSON.parse(response.data);
                }, function(response) {
                    console.log('rejection promise');
                    return $q.reject(response.data);
                });
        }

        function postRequestGeneric(pathParam, data) {
            var req = {
                method : 'POST',
                url : '/api/v1/' + pathParam,
                data : data
            }
            return $http(req).then(function(response) {
                return JSON.parse(response.data);
            }, function(response){
                console.log('rejecting promise');
                return $q.reject(response.data);
            });
        }

        function getCrime(id) {
            var req = {
                method: 'GET',
                url: '/api/v1/crimes/' + id
            }
            return $http(req).then(function(response) {
                return JSON.parse(response.data);
            }, function(response) {
                console.log('rejecting promise');
                return $q.reject(response.data);
            })
        }

        function getCrimeType(id) {
            var req = {
                method: 'GET',
                url: '/api/v1/crime_types/' + id
            }
            return $http(req).then(function(response) {
                return JSON.parse(response.data);
            }, function(response) {
                console.log('rejecting promise');
                return $q.reject(response.data);
            })
        }

        function getWeek(id) {
            var req = {
                method: 'GET',
                url: '/api/v1/weeks/' + id
            }
            return $http(req).then(function(response) {
                return JSON.parse(response.data);
            }, function(response) {
                console.log('rejecting promise');
                return $q.reject(response.data);
            })
        }

        function getZip(id) {
            var req = {
                method: 'GET',
                url: '/api/v1/zips/' + id
            }
            return $http(req).then(function(response) {
                return JSON.parse(response.data);
            }, function(response) {
                console.log('rejecting promise');
                return $q.reject(response.data);
            })
        }
    });

'use strict';

angular.module('crimeCastApp.httpServices', [])
    .factory('http_service', function($http, $q){
        return {
            getRequestGeneric : getRequestGeneric,
            postRequestGeneric : postRequestGeneric,
            getCrime : getCrime,
            getCrimeType : getCrimeType,
            getWeek : getWeek,
            getZip : getZip
        }

        function getRequestGeneric(pathParam){
            return $http
                .get(
                '/api/v1/' + pathParam ).then(function(response) {
                    return response.data;
                }, function(response){
                    console.log('rejecting promise');
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
                return response.data;
            }, function(response){
                console.log('rejecting promise');
                return $q.reject(response.data);
            });
        }

        function getCrime(id) {
            var req = {
                method: 'GET',
                url: '/api/v1/crime/' + id
            }
            return $http(req).then(function(response) {
                return response.data;
            }, function(response) {
                console.log('rejecting promise');
                return $q.reject(response.data);
            })
        }

        function getCrimeType(id) {
            var req = {
                method: 'GET',
                url: '/api/v1/crime_type/' + id
            }
            return $http(req).then(function(response) {
                return response.data;
            }, function(response) {
                console.log('rejecting promise');
                return $q.reject(response.data);
            })
        }

        function getWeek(id) {
            var req = {
                method: 'GET',
                url: '/api/v1/week/' + id
            }
            return $http(req).then(function(response) {
                return response.data;
            }, function(response) {
                console.log('rejecting promise');
                return $q.reject(response.data);
            })
        }

        function getZip(id) {
            var req = {
                method: 'GET',
                url: '/api/v1/zip/' + id
            }
            return $http(req).then(function(response) {
                return response.data;
            }, function(response) {
                console.log('rejecting promise');
                return $q.reject(response.data);
            })
        }
    });

'use strict';

angular.module('crimeCastApp.httpServices', [])
    .factory('http_service', function($http, $q){
        return {
            getRequestGeneric : getRequestGeneric,
            postRequestGeneric : postRequestGeneric,
            getCrime : getCrime
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
                url: '/api/v1/crimes/' + id
            }
            return $http(req).then(function(response) {
            }, function(response) {
                console.log('rejecting promise');
                return $q.reject(response.data);
            })
        }
    });

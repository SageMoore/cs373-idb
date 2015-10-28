angular.module('crimeCastApp.restServices', [])
    .factory('rest', function($http, $q){
        return {
            getRequestGeneric : getRequestGeneric,
            postRequestGeneric : postRequestGeneric
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
            }, function(response){
                console.log('rejecting promise');
                return $q.reject(response.data);
            });
        }
    });

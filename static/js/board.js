      'use strict';

      var app = angular.module('myApp', ['infinite-scroll']);
      app.constant('chunkSize', 20);

      app.controller('planetController', function($scope, $http, $log, $window, chunkSize) {

          $scope.images = [1, 2, 3, 4, 5, 6, 7, 8];

          $scope.loadMore = function() {
            $log.log('load...')
            var path = $window.location.pathname.split('/');
            $scope.board_name = path[2]
            $http.get("http://127.0.0.1:5000/api/" + path[2])
                    .success(function(response) {
                        for(let item of response) {
                            $log.log(item.href);
                        }

                        $scope.posts = response;
                        });
              };
        });



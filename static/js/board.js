      var app = angular.module('myApp', ['infinite-scroll']);

      app.controller('planetController', function($scope, $http, $log, $window) {
        var path = $window.location.pathname.split('/');
        $scope.board_name = path[2];
        $scope.parent = 'True';
        $scope.up = '';
        $scope.posts = [];

        $scope.loadMore = function() {
            if ($scope.busy) return;
            $scope.busy = true;

            var url = "/api/" + path[2] + '/' + $scope.up
            $http.get(url)
                .success(function(response) {
                    for(let i of response['text']){
                        $scope.posts.push(i);
                    };
//                  $scope.posts = response['text'];

                    $scope.up = response['up'];
                    $scope.busy = false;

            });
        }.bind($scope);

        $scope.loadMore();
        });


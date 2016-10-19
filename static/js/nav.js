      app.controller('cont_nav', function($scope, $http, $log, $location, $window) {

           $scope.parent = 'a';
           $scope.btn-parent = True;
        var path = $window.location.pathname.split('/');
        if (path.length > 0) {
           $log.log(path);
           $scope.parent = path[2];
        }
    });

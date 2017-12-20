  var app = angular.module('myApp', ['ngSanitize']);
  app.controller('planetController', function($scope, $http, $log, $location, $window) {
    var path = $window.location.pathname.split('/');

    $scope.board_name = path[2];
    $scope.parent = 'True';

    $http.get("/api/" + path[2] + '/' + path[3])
            .success(function(response) {
              $scope.author = response['作者'];
              $scope.time = response['時間'];
              $scope.title = response['標題'];

              var after_posts = [];

              var comment = false
              for(let post of response['text']) {
                var tag = post['tag'];
                var txt = '';
                if(tag){
                  comment = true
                  txt += "<span class='col-xs-2'>";
                  if(tag === '→ '){
                    txt += "<span class='label'>";
                  }else if(tag === '推 '){
                    txt += "<span class='label label-info'>";
                  }else if(tag === '噓 '){
                    txt += "<span class='label label-danger'>";
                  }

                  txt += tag + post['user'] + "  </span></span>";
                  txt += '<a>'
                  txt += String(post['text']).replace(/\n/g, "<br />");
                  txt += '</a>'
                  txt += "<span class='pull-right'>" + post['time'] + "</span>";
                } else if(comment){
                  txt += "<span class='col-xs-2'> </span> ";
                  txt += String(post['text']).replace(/\n/g, "<br />");
                  txt += "";
                } else {
                  txt += String(post['text']).replace(/\n/g, "<br />");
                }


                post['text'] = txt
                after_posts.push(post);
              }

              $scope.posts = after_posts;
            });
  });



